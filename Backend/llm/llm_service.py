from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from langchain_ollama import OllamaLLM
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# flow ของ nodeทั้งหมดจะมีหน้าตาแบบนี้
"""
(Start)
   |
   v
[ LLM Router ] ---> [ other ] ----------------------+
       |                                             |
       |--> [ retrieve ] --> [ generate response ] --+--> (End)
       |                                             |
       +--> [ general chat ] -----------------------+
"""

llm = OllamaLLM(model="scb10x/typhoon2.1-gemma3-4b")
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
memory = MemorySaver()

vectordb = Chroma(
    persist_directory="ลงทะเบียนchroma_db",
    embedding_function=embedding_model
)

class BasicChatState(TypedDict):
    messages: Annotated[list, add_messages]
    documents: list

#Node นี้คือการ define เส้นทางที่ Model สามารถเลือกได้ว่าจะไป route ไหนยังมีข้อจำกัดต้องเขียน prompt และคำถามให้รัดกุม
def llm_router_tool(state: BasicChatState):
    decision_route = state["messages"][-1].content
    prompt = f"""
    จงพิจารณาคำถามต่อไปนี้ : {decision_route}"

    ตอบเพียงคำเดียวจากตัวเลือก
    - general_chat -> ถ้าเป็นคำทักทาย, แนะนำตัว, คำถามทั่วไป, การสนทนาต่อเนื่อง, หรือคำถามเกี่ยวกับประวัติการสนทนา
    - retrieve -> ถ้าเป็นคำถามเกี่ยวกับ การลงทะเบียน/เพิ่มถอน/หอพัก/กยศ
    - other -> ถ้าไม่เข้าเงื่อนไขใดเลย (ให้ตอบ ไม่พบข้อมูลที่เกี่ยวข้องในระบบ คุณสามารถถามคำถามที่เกี่ยวข้องกับ หอพัก, การลงทะเบียน เพิ่ม-ถอน, หรือ กยศได้เป็นต้น)
    """ 
    result = llm.invoke(prompt).strip().lower()
    print("route decision", result)
    return result if result in ["general_chat", "retrieve"] else "other"

#Node นี้คือการดึง document จากข้อความผู้ใช้ เอาเฉพาะข้อความล่าสุดเท่านั้น
def retrieve(state: BasicChatState):
    """โหนดนี้ใช้ค้นหาเอกสารจาก Vectordb"""
    
    # ดึงข้อความล่าสุด (คำถามของผู้ใช้)
    # .content เพื่อให้ได้แค่ข้อความ string
    user_query = state["messages"][-1].content
    
    # ทำการค้นหาใน Vectordb
    # results มี format เป็น list ของ (document, score)
    results = vectordb.similarity_search_with_score(
        user_query, 
        k=3
    )
    
    # ส่งผลลัพธ์การค้นหาไปอัปเดต State
    return {"documents": results}

#Node นี้จะดำเนินหลังจาก retrive เสร็จจะสร้างคำตอบด้วยกระบวนการ Rag ปกติ
def generate_response(state: BasicChatState):
    """โหนดนี้ใช้ LLM สร้างคำตอบโดยอ้างอิงจากเอกสารที่ค้นเจอ"""
    # 1. จัดรูปแบบ Context จากเอกสาร
    context = "\n---\n".join([doc.page_content for doc, score in state["documents"]])
    
    # 2. ดึงประวัติการสนทนาทั้งหมด
    history = state["messages"][:-1] # ประวัติเก่า (ไม่รวมคำถามล่าสุด)
    latest_query = state["messages"][-1].content # คำถามล่าสุด
    
    # 3. สร้าง Prompt สำหรับ RAG
    # เราใช้ SystemMessage เพื่อให้ LLM รับรู้ถึงบริบท RAG
    rag_prompt = [
        SystemMessage(content=f"""คุณคือผู้ช่วย AI ภายในมหาวิทยาลัยศิลปากรที่ตอบคำถามด้วยความสุภาพจากบริบทที่กำหนดให้
                      จงใช้ 'เอกสารอ้างอิง' ในการตอบคำถามล่าสุดของผู้ใช้
                      ถ้าหากเอกสารอ้างอิงไม่มีข้อมูลที่เกี่ยวข้อง ให้ตอบว่า 'ไม่พบข้อมูลที่เกี่ยวข้องในระบบ คุณสามารถถามคำถามที่เกี่ยวข้องกับ หอพัก, การลงทะเบียน เพิ่ม-ถอน, หรือ กยศได้เป็นต้น'

                      เอกสารอ้างอิง:
                      {context}"""),
        *history,
        HumanMessage(content=latest_query) # คำถามล่าสุดของผู้ใช้
    ]
    
    # 4. Invoke LLM ด้วย Prompt ที่สร้างจาก RAG
    response = llm.invoke(rag_prompt)
    
    # คืนคำตอบกลับไปอัปเดต State (ผ่าน add_messages)
    return {"messages": [AIMessage(content=response)]}

#Node นี้คือเส้นทางหากต้องการคุยทั่วไป แนะนำตัว หรือถามคำถามทั่วไป, การสนทนาต่อเนื่องหรือเกี่ยวกับประวัติแชท 
#ต้องถามให้รัดกุมนะรู้สึก model จะยังสับสนและแยกไม่ออกในบางที
def general_chat(state: BasicChatState):
    """โหนดสำหรับตอบคำถามทั่วไป (ถ้ามี Router)"""
    #"--- 💬 กำลังตอบคำถามทั่วไป ---"
    response = llm.invoke(state["messages"])
    return {"messages": [AIMessage(content=response)]}

#nodeนี้คือเส้นทางสุดท้ายถ้าหาก model เลือกไม่ถูกว่าจะตอบในเส้นทางไหน แต่พวกคำถาม คำถามทั่วไป, การสนทนาต่อเนื่อง, หรือคำถามเกี่ยวกับประวัติการสนทนา 
#ต้องถามให้รัดกุมนะรู้สึก model จะยังสับสนและแยกไม่ออกอาจทำให้หล่นในช่องนี้ได้
def other_response(state: BasicChatState):
    response = "ไม่พบข้อมูลที่เกี่ยวข้องในระบบ คุณสามารถถามคำถามที่เกี่ยวข้องกับ หอพัก, การลงทะเบียน เพิ่ม-ถอน, หรือ กยศได้เป็นต้น"
    return {"messages": [AIMessage(content=response)]}

#ตอนสร้าง instance ของ graph จะต้องใส่ format ขอข้อความที่ llm มันจะต้องรับในที่นี้คือ format ของ class BasicChatState
graph = StateGraph(BasicChatState)

graph.add_node("retrieve", retrieve)
graph.add_node("general_chat",general_chat)
graph.add_node("generate", generate_response) 
graph.add_node("other", other_response)

graph.set_conditional_entry_point(llm_router_tool,{
    "retrieve" : "retrieve",
    "general_chat" : "general_chat",
    "other": "other"
})

graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)
graph.add_edge("general_chat",END)
graph.add_edge("other", END)

app = graph.compile(checkpointer=memory)

#ส่วนนี้อาจจะต้องเปลี่ยนไปตาม session id ของผู้ใช้อาจจะต้องมาปรับแก้อีกทีในตอนเข้า api endpoint
config = {"configurable": {
    "thread_id": 1
}}

def LLMChat(message):
    res = app.invoke({
        "messages": HumanMessage(content=message)
    }, config=config)
    # ไม่มีอะไรมาก return ข้อความล่าสุดใน list
    return res["messages"][-1].content

