from fastapi import APIRouter, Request, Header, HTTPException
import os
from pathlib import Path
from dotenv import load_dotenv
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent,PostbackEvent,FollowEvent
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

from app.services.llm.test_chat_rag_memory import chat_rag_memory
from app.crud.conversation import save_conversation,update_daily_stats
from app.crud.user import is_new_line_user

router = APIRouter(prefix="", tags=["line"])

client = chromadb.PersistentClient(path="app/services/llm/chroma_db")  #ดู path folderให้ถูกต้อง
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
vector_store_from_client = Chroma(
    client=client,
    collection_name="rag_documents",
    embedding_function=embedding_model,
)

load_dotenv()
#ลายเซ็นที่ไลน์มอบให้เรา เพื่อบอกว่าข้อมูลที่ส่งมาหาบอทเรา มาจากไลน์จริงๆ
get_channel_secret = os.getenv('CHANNEL_SECRET')
#บัตรผ่านทางเผื่อดูว่ามีสิทธิ์ส่งข้อมูลไปหา lineผู้ใช้
get_access_token = os.getenv('ACCESS_TOKEN')

configuration = Configuration(access_token=get_access_token)
handler = WebhookHandler(channel_secret=get_channel_secret)

@router.post("/line-chat")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    body_str = body.decode('utf-8')
    # print(body_str)
    # print(x_line_signature)
    try:
        handler.handle(body_str, x_line_signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        raise HTTPException(status_code=400, detail="Invalid signature.")

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    line_user_id = event.source.user_id #ใช้สำหรับ thread_id
    question = event.message.text
    print("question: ",question)
    
    response = chat_rag_memory(question,vector_store_from_client,line_user_id) 
    answer = response["ai_message"]
        
    reply_message = TextMessage(text=answer)

    with ApiClient(configuration) as api_client:#เปิดการเชื่อมต่อ
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[reply_message]
            )
        )
    save_conversation(line_user_id,"LINE",response)
    update_daily_stats("LINE",response)
    

@handler.add(PostbackEvent)
def handle_postback(event):#กด richmenu
    rich_menu_data = event.postback.data
    if rich_menu_data == 'action=A':
        reply_message = """💡 **หัวข้อคำถามเพิ่มเติม**

นักศึกษาสามารถพิมพ์คำถามที่สงสัยเกี่ยวกับเรื่องดังต่อไปนี้ได้เลยครับ

• ขั้นตอนการลงทะเบียนเรียน 
• การลงทะเบียนเรียน (ล่าช้า) 
• การเพิ่มถอน เปลี่ยนกลุ่มเรียน 
• การดูผลการลงทะเบียนเรียน 
• ตรวจสอบภาระค่าใช้จ่าย 
• การขอสำรองที่นั่งออนไลน์ 
• คำร้องขอติด W ออนไลน์ 
• ตรวจสอบคำร้อง 
• Email แจ้งเตือนคำร้อง 
• ใบคำร้องสำหรับนักศึกษาปริญญาตรี 

👇 ลองพิมพ์คำถามของคุณทิ้งไว้ได้เลย!"""
    elif rich_menu_data == 'action=B':
        reply_message = """💻 **หัวข้อคำถามเพิ่มเติม**

นักศึกษาสามารถพิมพ์คำถามที่สงสัยเกี่ยวกับเรื่องดังต่อไปนี้ได้เลยครับ

• วิธีกู้คืน SU-IT Account 
• วิธีลงทะเบียน SU-IT Account  

👇 ลองพิมพ์คำถามของคุณทิ้งไว้ได้เลย!"""
    elif rich_menu_data == 'action=C':
        reply_message = """🏢 **หัวข้อคำถามเพิ่มเติม**

นักศึกษาสามารถพิมพ์คำถามที่สงสัยเกี่ยวกับเรื่องดังต่อไปนี้ได้เลยครับ

• คุณสมบัติของผู้กู้ยืมกยศ.(กู้ยืมเพื่อการศึกษา) 
• ประเภทของผู้กู้ยืมเงิน 
• คุณสมบัติทั่วไปของนักศึกษาผู้กู้ยืมเงินกองทุน 
• ลักษณะต้องห้ามของนักศึกษาผู้กู้ยืมเงินกองทุน 
• คุณสมบัติเฉพาะของนักศึกษาผู้กู้ยืมเงินกองทุน ลักษณะที่ 1,2 และ 3
• หอพักนักศึกษา

👇 ลองพิมพ์คำถามของคุณทิ้งไว้ได้เลย!"""
    
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
        )

@handler.add(FollowEvent)
def handle_follow(event):#เพิ่มเพื่อนครั้งแรก
    line_user_id = event.source.user_id
    created = is_new_line_user(line_user_id)#เช็คว่าผู้ใช้ใหม่ไหม ถ้าใหม่อัปเดตเข้า table Users
    if created:
        print("new line user:",line_user_id)
    else:
        print("old line user:",line_user_id)
    
    welcome_message = """สวัสดีครับ! ขอบคุณที่เพิ่มเพื่อนกับ SU AskMe FAQ นะครับ 🤖✨
เราเป็นแชตบอตที่สร้างขึ้นเพื่อตอบคำถามที่พบบ่อยให้กับนักศึกษาภายในมหาวิทยาลัยศิลปากร
โดยมีหัวข้อคำถามดังนี้ครับ

• การลงทะเบียนเรียน 
• การเพิ่มถอนรายวิชา 
• เอกสารคำร้อง 
• SU-IT Account
• กยศ.
• หอพัก

หากต้องการดูหัวข้อคำถามเพิ่มเติมสามารถกดที่เมนูด้านล่างหรือพิมพ์คำถามของคุณได้เลยครับ! 👇"""
    
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=welcome_message)]
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

        with open('app/images/line-chatbot-rich-menu.jpg', 'rb') as f:
            line_bot_blob_api.set_rich_menu_image(
                rich_menu_id=rich_menu_id,
                body=f.read(),
                _headers={'Content-Type': 'image/jpeg'}
            )
        
        line_bot_api.set_default_rich_menu(rich_menu_id=rich_menu_id)
        print("สร้าง rich menu แล้ว")

# create_su_askme_rich_menu() #ถ้าจะแก้ฟังชันนี้ค่อย uncomment


#.venv\Scripts\activate
#uvicorn app.main:app --reload

#ถ้าใช้ไลน์ด้วยรัน ngrok http --url=suzan-uneloquent-grossly.ngrok-free.dev 8000
#ไม่ต้องเปลี่ยนที่ line console แล้ว