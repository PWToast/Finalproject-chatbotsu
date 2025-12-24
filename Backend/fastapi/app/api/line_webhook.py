from fastapi import APIRouter, Request, Header, HTTPException
import os
from pathlib import Path
from dotenv import load_dotenv
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent,PostbackEvent
from linebot.v3.messaging import (
    ApiClient, 
    MessagingApi, 
    Configuration, 
    ReplyMessageRequest, 
    TextMessage,
    MessagingApiBlob,
    RichMenuRequest,
    RichMenuArea,
    RichMenuSize,
    RichMenuBounds,
    PostbackAction
)

import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from app.services.users.line_user import ensure_line_user
from app.services.llm.test_chat_rag_memory import chat_rag_memory

router = APIRouter(prefix="/line", tags=["line"])

client = chromadb.PersistentClient(path="app/services/llm/chroma_db")  #ดู path folderให้ถูกต้อง
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
vector_store_from_client = Chroma(
    client=client,
    collection_name="chatbot_rag_documents",
    embedding_function=embedding_model,
)

ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)
get_channel_secret = os.getenv('CHANNEL_SECRET')
get_access_token = os.getenv('ACCESS_TOKEN')

# def get_secret_value(secret_name, default=None):
#     secret_path = f"/secrets/{secret_name}"
#     if os.path.exists(secret_path):  
#         with open(secret_path, "r") as f:
#             return f.read().strip()
#     return os.getenv(secret_name, default)

# get_access_token = get_secret_value('ACCESS_TOKEN')
# get_channel_secret = get_secret_value('CHANNEL_SECRET')

configuration = Configuration(access_token=get_access_token)
handler = WebhookHandler(channel_secret=get_channel_secret)

@router.post("/chat")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    body_str = body.decode('utf-8')
    # print(body_str)
    try:
        handler.handle(body_str, x_line_signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        raise HTTPException(status_code=400, detail="Invalid signature.")

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    line_user_id = event.source.user_id #ใช้สำหรับ thread_id
    # print("line_user_id: ",line_user_id)
    created = ensure_line_user(line_user_id)#เช็คว่าผู้ใช้ใหม่ไหม
    if created:
        print("new line user:",line_user_id)
    else:
        print("old line user:",line_user_id)
    question = event.message.text
    print("question: ",question)
    
    answer,category = chat_rag_memory(question,vector_store_from_client,line_user_id) 
    
        
    reply_message = TextMessage(text=answer)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[reply_message]
            )
        )
    # save_conversation(user_id,question,answer,category,"LINE")
    

@handler.add(PostbackEvent)
def handle_postback(event):
    rich_menu_data = event.postback.data
    if rich_menu_data == 'action=A':
        reply_message = """💡 **แนะนำการถามคำถาม**

นักศึกษาสามารถพิมพ์คำถามที่สงสัยเกี่ยวกับเรื่องดังต่อไปนี้ได้เลยครับ:

• การลงทะเบียน เช่น ลงทะเบียนล่าช้าทำยังไง, ขั้นตอนการลงทะเบียน
• การเพิ่มถอน เช่น ถอนรายวิชาติด W ทำยังไง, สาเหตุการลงทะเบียนเพิ่มถอนไม่ได้
• การขอใบคำร้อง เช่น ขอใบลาออกได้ที่ไหน, ต้องการลาพักการศึกษาต้องทำยังไง

👇 พิมพ์คำถามของคุณทิ้งไว้ได้เลย!"""
    elif rich_menu_data == 'action=B':
        reply_message = """💻 **แนะนำการถามคำถาม**

นักศึกษาสามารถพิมพ์คำถามที่สงสัยเกี่ยวกับเรื่องดังต่อไปนี้ได้เลยครับ:

• SU-IT Account เช่น ลืมรหัสผ่าน su it account ทำยังไง, การกู้คืนบัญชี su it account ทำอย่างไรได้บ้าง
• การใช้งานคอมพิวเตอร์ เช่น สิทธิ์การปริ้นงานของนักศึกษา

👇 พิมพ์คำถามของคุณทิ้งไว้ได้เลย!"""
    elif rich_menu_data == 'action=C':
        reply_message = """🏢 **แนะนำการถามคำถาม**

นักศึกษาสามารถพิมพ์คำถามที่สงสัยเกี่ยวกับเรื่องดังต่อไปนี้ได้เลยครับ:

• กยศ. เช่น ผู้กู้รายเก่าคืออะไร, สาขาที่เป็นความต้องการหลักคืออะไร, อยู่ปี4แล้วยังต้องเก็บชั่วโมงจิตอาสาไหม
• หอพักนักศึกษา เช่น ข้อปฏิบัติของหอพัก, การเตรียมความพร้อมเข้าหอพักนักศึกษา

👇 พิมพ์คำถามของคุณทิ้งไว้ได้เลย!"""
    
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
        )

def create_su_askme_rich_menu():
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_blob_api = MessagingApiBlob(api_client)

        rich_menu_request = RichMenuRequest(
            size=RichMenuSize(width=2500, height=1686),
            selected=True,
            name="SU_AskMe_FAQ_Menu",
            chat_bar_text="เมนูสอบถาม",
            areas=[
                
                RichMenuArea( #A
                    bounds=RichMenuBounds(x=0, y=843, width=833, height=843),
                    action=PostbackAction(data="action=A", label="A")
                ),
                RichMenuArea( #B
                    bounds=RichMenuBounds(x=833, y=843, width=834, height=843),
                    action=PostbackAction(data="action=B", label="B")
                ),
                RichMenuArea( #C
                    bounds=RichMenuBounds(x=1667, y=843, width=833, height=843),
                    action=PostbackAction(data="action=C", label="C")
                )
            ]
        )

        rich_menu_response = line_bot_api.create_rich_menu(rich_menu_request=rich_menu_request)
        rich_menu_id = rich_menu_response.rich_menu_id
        print(f"Rich Menu ID: {rich_menu_id}")

        with open('images/line-chatbot-rich-menu.jpg', 'rb') as f:
            line_bot_blob_api.set_rich_menu_image(
                rich_menu_id=rich_menu_id,
                body=f.read(),
                _headers={'Content-Type': 'image/jpeg'}
            )
        
        line_bot_api.set_default_rich_menu(rich_menu_id=rich_menu_id)
        print("สร้าง rich menu แล้ว")

#create_su_askme_rich_menu() ถ้าจะแก้ฟังชันนี้ค่อย uncomment


#.venv\Scripts\activate
#uvicorn test_api:app --reload

#ใช้ไลน์ รัน ngrok http 8000 เปลี่ยนลิ้งค์เอาลิ้งไปเปลี่ยนที่console