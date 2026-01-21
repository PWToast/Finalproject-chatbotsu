from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from langchain_ollama import OllamaLLM
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

llm = OllamaLLM(model="scb10x/typhoon2.1-gemma3-4b")
memory = MemorySaver()
# client = chromadb.PersistentClient(path="chroma_db")  #ดู path folderให้ถูกต้อง
# embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
# vector_store_from_client = Chroma(
#     client=client,
#     collection_name="rag_documents",#เปลี่ยนชื่อ collectionให้ถูกต้อง
#     embedding_function=embedding_model,
# )
class BasicChatState(TypedDict):
    messages: Annotated[list, add_messages]
    rewritten_question: str
    documents: list
    agency: str 
    route_decision: str
    is_fallback: bool 

def get_route(state: BasicChatState):
    route = state.get("route_decision", "other")
    return route

def agency_check(state: BasicChatState):#อาจจะต้องไปใส่ทีหลัง เพราะมีการ rewrite
    question = state["rewritten_question"]
    agency_check_prompt = f"""
จงพิจารณาคำถามต่อไปนี้: "{question}"

**สำคัญมาก:** ตอบเพียงตัวเลือกเดียวจากตัวเลือกต่อไปนี้ว่าอยู่ในหมวดไหน ตอบแค่ชื่อหมวดเท่านั้น

- กองบริหารวิชาการ -> ถ้าคำถามเกี่ยวกับ การลงทะเบียน เพิ่มถอนรายวิชา การยื่นขอใบคำร้องต่างๆ การใช้งานเว็บไซต์ reg ของมหาวิทยาลัยศิลปากร
- สำนักดิจิทัลเทคโนโลยี -> ถ้าคำถามเกี่ยวกับ การใช้งานบริการคอมพิวเตอร์ การพิมพ์เอกสาร การใช้งาน SU-IT Account ของมหาวิทยาลัยศิลปากร
- กองกิจการนักศึกษา -> ถ้าคำถามเกี่ยวกับ กยศ(กองทุนให้กู้ยืมเพื่อการศึกษา) หอพักนักศึกษา ของมหาวิทยาลัยศิลปากร
- อื่นๆ -> **ถ้าคำถามเป็น** คำถามทั่วไป, คำถามส่วนตัว, คำถามที่เกี่ยวข้องกับการทำงานของบอท, **หรือคำถามที่ต้องการให้ทบทวนบทสนทนา เช่น 'เมื่อกี้ถามอะไรไปบ้าง'** ถ้าเข้าข่ายนี้ให้เลือก 'อื่นๆ' ทันที ไม่ว่าคำถามก่อนหน้าจะอยู่ในหมวดใดก็ตาม
"""
    # print("agency_check_prompt: ",agency_check_prompt)
    result =  llm.invoke(agency_check_prompt).strip()
    if result not in ["กองบริหารวิชาการ","สำนักดิจิทัลเทคโนโลยี","กองกิจการนักศึกษา","อื่นๆ"]:
        # print("not in any agency")
        result = "อื่นๆ"
    # print('หมวด: ', result)
    return {"agency": result} 

def llm_decision(state: BasicChatState):
    recent_messages = state["messages"][-7:-1] #เอา3ประวัติสนทนาล่าสุด ยกเว้นคำถามล่าสุด
    # print(f"recent_messages:\n{recent_messages}")
    
    history = ""
    if recent_messages: #ถ้ามีข้อมูล
        #จัดformatt เอา3ประวัติสนทนาล่าสุด ยกเว้นคำถามล่าสุด
        for msg in recent_messages: 
            role = "User" if isinstance(msg, HumanMessage) else "AI"
            history += f"{role}: {msg.content}\n"

    user_question = state["rewritten_question"]

    decision_prompt = [
    SystemMessage(content=f"""คุณคือผู้เชี่ยวชาญด้านการจัดประเภทคำถามที่เกี่ยวข้องกับ การลงทะเบียน เพิ่มถอนรายวิชา การยื่นขอใบคำร้อง การใช้งานเว็บไซต์ reg 
การใช้งานบริการคอมพิวเตอร์ การพิมพ์เอกสาร การใช้งาน SU-IT Account กยศ(กู้ยืมเพื่อการศึกษา) การเก็บชั่วโมงจิตอาสา หอพักนักศึกษา 
คุณมีหน้าที่ตัดสินใจว่าจะส่งต่อคำถามล่าสุดไปที่ขั้นตอนใด
    
คุณต้องตอบกลับด้วย 'คำสั่งเดียว' จากตัวเลือกต่อไปนี้เท่านั้น:
    
1. **retrieve**: ถ้าคำถามล่าสุดเป็นคำถาม 'ใหม่' หรือ 'โดดเดี่ยว' ที่ไม่ต้องการบริบทใดๆ แต่ต้องการข้อมูลจากฐานความรู้
2. **general**: ถ้าคำถามล่าสุดเป็นคำถาม 'ทักทาย' หรือ 'พูดคุยทั่วไป' อยู่ในขอบเขตที่เชี่ยวชาญ ซึ่งรวมถึงคำถามประเภท 'การจัดการบริบท/การทบทวนบทสนทนา/ถามข้อมูลแชทบอท' เช่น 'เมื่อกี้ถามอะไรไปบ้าง', 'คุณตอบว่าอะไรนะ', 'คุณเป็นใคร'
3. **other**: เลือกคำนี้ **ถ้าคำถามไม่เข้าข่ายทั้ง 'retrieve' และ 'general' เลย หรือ คำถามที่ไม่เกี่ยวข้องกับขอบเขตความเชี่ยวชาญ
                  
**กฎที่ต้องปฏิบัติตามอย่างเคร่งครัด:**
* **ห้ามตอบคำถามอื่นใดนอกจากคำสั่งเดียวที่เลือกจาก 3 ตัวเลือกข้างต้น (retrieve, general, other)**
* **ห้ามมีคำอธิบาย, เครื่องหมายวรรคตอน, หรือข้อความเพิ่มเติมใดๆ ทั้งสิ้น**
    
ตัวอย่างการตอบที่ถูกต้อง:
retrieve
    
ตัวอย่างการตอบที่ถูกต้อง:
general

ตัวอย่างการตอบที่ถูกต้อง:
other             

**ประวัติการสนทนา:**
{history}                 
"""),
    HumanMessage(content=f"คำถามล่าสุด: {user_question}")
]
    # print(decision_prompt)
    route = llm.invoke(decision_prompt).strip()
    if route not in ["retrieve","general","other"]:
        # print("not in any route")
        route = "other"
    # print('ตัดสินใจ: ', route)
    return {"route_decision": route}

def rewrite_query(state: BasicChatState):
    recent_messages = state["messages"][-7:-1] #เอา3ประวัติสนทนาล่าสุด ยกเว้นคำถามล่าสุด
    # print(f"recent_messages:\n{recent_messages}")
    
    history = ""
    if recent_messages: #ถ้ามีข้อมูล
        #จัดformatt เอา3ประวัติสนทนาล่าสุด ยกเว้นคำถามล่าสุด
        for msg in recent_messages: 
            role = "User" if isinstance(msg, HumanMessage) else "AI"
            history += f"{role}: {msg.content}\n"

    recent_question = state["messages"][-1]
    user_question = recent_question.content
    #ถ้าไม่มีประวัติไม่ต้อง Rewrite
    if not history:
        # print("ไม่พบประวัติสนทนา ไม่ต้อง rewrite")
        #ไม่ต้องอัปเดตอะไร
        return {"rewritten_question": user_question}#ใช้คำถามต้นฉบับ
    
    # print(f"format ประวัติสนทนา:\n{history}")

    rewrite_prompt = [
    SystemMessage(content=f"""คุณคือผู้เชี่ยวชาญด้าน Search Query Refinement หน้าที่ของคุณคือสร้าง 'คำถามภาษาไทย' ที่สมบูรณ์แบบ (Standalone Question) เพื่อใช้สำหรับค้นหาในฐานข้อมูล

**หลักการทำงาน:**
1. วิเคราะห์ Context จากประวัติการสนทนา เพื่อเติมเต็มส่วนที่ขาดหายในคำถามล่าสุด
2. แก้ไขสรรพนามและคำกำกวม (เช่น "อันนั้น", "ที่นั่น", "เท่าไหร่", "กี่บาท") ให้กลายเป็นคำนามที่ชัดเจน
3. หากคำถามล่าสุดสมบูรณ์และเข้าใจได้ในตัวมันเองอยู่แล้ว ให้ส่งคำถามเดิมกลับมา ไม่ต้องแก้ไขใดๆ
4. หากคำถามล่าสุดไม่เกี่ยวข้องกับประวัติสนทนาก่อนหน้าหรือเปลี่ยนประเด็น ให้ส่งคำถามเดิมกลับมา ไม่ต้องแก้ไขใดๆ
5. ถ้าคำถามล่าสุดเป็นคำถาม 'ทักทาย' หรือ 'พูดคุยทั่วไป' ซึ่งรวมถึงคำถามประเภท 'การจัดการบริบท/การทบทวนบทสนทนา' เช่น 'เมื่อกี้ถามอะไรไปบ้าง', 'คุณตอบว่าอะไรนะ' ให้ส่งคำถามเดิมกลับมา ไม่ต้องแก้ไขใดๆ
6. **Output:** ตอบเฉพาะตัว "คำถาม" ที่ปรับปรุงแล้วเท่านั้น ห้ามอธิบาย ห้ามใส่ "คำถามคือ:" หรือใส่เครื่องหมายอัญประกาศและห้ามมี prefix

**ประวัติการสนทนา:**
{history}

ตัวอย่างที่ 1:
- ประวัติสนทนา: "นักศึกษาจำเป็นต้องลงทะเบียนเรียนให้ถึงเกณฑ์หน่วยกิตขั้นต่ำ"
- คำถามล่าสุด: "กี่หน่วยกิต"
- ผลลัพธ์: "หน่วยกิตขั้นต่ำในการลงทะเบียนเรียนคือกี่หน่วยกิต"

ตัวอย่างที่ 2:
- ประวัติสนทนา: "หลักสูตรวิทยาการคอมพิวเตอร์เรียนทั้งหมด 4 ปี"
- คำถามล่าสุด: "ค่าเทอมเท่าไหร่"
- ผลลัพธ์: "ค่าธรรมเนียมการศึกษาของหลักสูตรวิทยาการคอมพิวเตอร์เท่าไหร่"

ตัวอย่างที่ 3:
- ประวัติสนทนา: "หากสงสัยเพิ่มเติมสามารถติดต่อกองบริหารวิชาการ"
- คำถามล่าสุด: "ติดต่อได้ที่ไหน"
- ผลลัพธ์: "ติดต่อกองบริหารวิชาการได้ที่ไหน"
"""),
    HumanMessage(content=f"คำถามล่าสุด: {user_question}")
]#อาจต้องกำหนดสรรพนามเพิ่ม
    # print("rewrite_prompt: ",rewrite_prompt)
    rewritten_question = llm.invoke(rewrite_prompt).strip()
    # print("คำถามต้นฉบับ: ",user_question)
    # print("คำถามที่ rewrite: ",rewritten_question)
    #แทนที่คำถามล่าสุดให้เป็นอันที่ rewrite
    return {"messages": [HumanMessage(content=rewritten_question,id=recent_question.id)],
            "rewritten_question": rewritten_question}

#Node นี้คือการดึง document จากข้อความผู้ใช้ เอาเฉพาะข้อความล่าสุดเท่านั้น
def retrieve(state: BasicChatState,config):
    
    user_query = state["rewritten_question"]
    # print("user_query at retrieve: ",user_query)
    vectordb = config.get("configurable", {}).get("embedding_model")
    results = vectordb.similarity_search_with_score(
        user_query, 
        k=5
    )

    return {"documents": results}

def generate_response(state: BasicChatState):

    
    # print("เนื้อหาที่ได้จากvectorDB:")
    context = ""
    for doc, score in state["documents"]:
        # print(f"\n{doc.page_content}")
        # print(f"score (Distance): {score:.4f}")
        # print("-" * 20)
        #เก็บข้อความ
        context += doc.page_content + "\n-----------"

    recent_messages = state["messages"][-7:-1] #เอา3ประวัติสนทนาล่าสุด ยกเว้นคำถามล่าสุด
    # print(f"recent_messages:\n{recent_messages}")
    
    history = ""
    if recent_messages: #ถ้ามีข้อมูล
        #จัดformatt เอา3ประวัติสนทนาล่าสุด ยกเว้นคำถามล่าสุด
        for msg in recent_messages: 
            role = "User" if isinstance(msg, HumanMessage) else "AI"
            history += f"{role}: {msg.content}\n"
    
    user_question = state["rewritten_question"]
    # print("user_query at generate: ",latest_query)
    rag_prompt = [
        SystemMessage(content=f"""คุณเป็นผู้เชี่ยวชาญด้านการตอบคำถามให้กับนักศึกษา โดยใช้ข้อมูลจาก "เอกสารอ้างอิง" ที่ได้รับเท่านั้น โดยดูจากความเกี่ยวข้องกับคำถามมากที่สุด 

**หลักการทำงาน:**
1. ตอบคำถามโดยใช้ข้อมูลจาก "เอกสารอ้างอิง" ที่ได้รับ
2. ใช้ "ประวัติสนทนา" เพื่อทำความเข้าใจบริบทว่าปัจจุบันกำลังคุยเรื่องอะไร แต่ไม่ต้องนำมาปนเป็นเนื้อหาคำตอบหากไม่จำเป็น
3. ถ้าหากเอกสารอ้างไม่มีข้อมูลที่เกี่ยวข้องกับคำถาม ให้ตอบแค่ข้อความนี้ 'Unknown'
4. ห้ามขึ้นต้นตอบด้วย "AI:" หรือ "Assistant:" หรือ prefix ใด ๆ ให้ตอบเฉพาะข้อความเท่านั้น

เอกสารอ้างอิง:
{context}

ประวัติสนทนา:
{history}
"""),
        HumanMessage(content=f"คำถามล่าสุด: {user_question}") # คำถามล่าสุดของผู้ใช้
    ]
    # print("rag_prompt ",rag_prompt)
    response = llm.invoke(rag_prompt)
    # print("คำตอบที่ได้จาก LLM:\n",response)
    fallback_message = "Unknown"
    agency = state["agency"]
    is_fallback = False
    if response == fallback_message:
        agency = "อื่นๆ"
        response = "ขออภัยครับ ผมยังไม่มีข้อมูลในส่วนนี้ คุณสามารถลองสอบถามเรื่อง การลงทะเบียน, เพิ่ม-ถอน, บริการคอมพิวเตอร์, กยศ. หรือเรื่องหอพัก แทนได้นะครับ หากมีข้อสงสัยอื่นเพิ่มเติม พิมพ์ถามใหม่ได้เลยครับ"
        is_fallback = True
    # print("หมวดปัจจุบัน: ", agency)
    # print(f"คำตอบสุดท้าย:\n{response}\n")
    return {"messages": [AIMessage(content=response)],"agency": agency,"is_fallback":is_fallback}

#Node นี้คือเส้นทางหากต้องการคุยทั่วไป แนะนำตัว หรือถามคำถามทั่วไป, หรือเกี่ยวกับประวัติแชท 
#ต้องถามให้รัดกุมนะรู้สึก model จะยังสับสนและแยกไม่ออกในบางที
def general_chat(state: BasicChatState):
    #ตอบคำถามทั่วไป
    recent_messages = state["messages"][-7:-1] #เอา3ประวัติสนทนาล่าสุด ยกเว้นคำถามล่าสุด
    # print(f"recent_messages:\n{recent_messages}")
    
    history = ""
    if recent_messages: #ถ้ามีข้อมูล
        #จัดformatt เอา3ประวัติสนทนาล่าสุด ยกเว้นคำถามล่าสุด
        for msg in recent_messages: 
            role = "User" if isinstance(msg, HumanMessage) else "AI"
            history += f"{role}: {msg.content}\n"

    user_question = state["rewritten_question"]
    general_prompt = [
        SystemMessage(content=f"""คุณเป็นผู้ช่วยตอบคำถามทั่วไปให้กับนักศึกษา ชื่อว่า "SU AskMe FAQ" เรียกแทนตัวเองว่า "น้องบอท" คุณมีหน้าตอบคำถามทั่วไปให้นักศึกษาโดยใช้ "ประวัติสนทนา" อ้างอิงเท่านั้น

**หลักการทำงาน:**
1. ตอบเป็นภาษาที่สุภาพ เข้าใจง่าย เหมาะกับนักศึกษา สามารถตอบด้วยอิโมจิได้ 
2. ห้ามตอบข้อมูลที่เกี่ยวกับโมเดล Typhoon และคุณไม่มีความเกี่ยวข้องกับ SCBX10
3. ห้ามขึ้นต้นคำตอบด้วย "AI:" หรือ "Assistant:" หรือ prefix ใด ๆ ให้ตอบเฉพาะข้อความเท่านั้น
                      
ประวัติสนทนา:
{history}
"""),
        HumanMessage(content=f"คำถามล่าสุด: {user_question}") # คำถามล่าสุดของผู้ใช้
    ]
    # print(general_prompt)
    response = llm.invoke(general_prompt)
    agency = "อื่นๆ"
    # print("หมวดปัจจุบัน: ", agency)
    # print(f"คำตอบสุดท้าย:\n{response}\n")
    return {"messages": [AIMessage(content=response)],"agency": agency}

#nodeนี้คือเส้นทางสุดท้ายถ้าหาก model เลือกไม่ถูกว่าจะตอบในเส้นทางไหน แต่พวกคำถาม คำถามทั่วไป, การสนทนาต่อเนื่อง, หรือคำถามเกี่ยวกับประวัติการสนทนา 
#ต้องถามให้รัดกุมนะรู้สึก model จะยังสับสนและแยกไม่ออกอาจทำให้หล่นในช่องนี้ได้
def other_response(state: BasicChatState):
    response = "ขออภัยครับ ผมยังไม่มีข้อมูลในส่วนนี้ คุณสามารถลองสอบถามเรื่อง การลงทะเบียน, เพิ่ม-ถอน, บริการคอมพิวเตอร์, กยศ. หรือเรื่องหอพัก แทนได้นะครับ หากมีข้อสงสัยอื่นเพิ่มเติม พิมพ์ถามใหม่ได้เลยครับ"
    agency = "อื่นๆ"
    is_fallback = True
    # print("หมวดปัจจุบัน: ", agency)
    # print(f"คำตอบสุดท้าย:\n{response}\n")
    return {"messages": [AIMessage(content=response)],"agency": agency,"is_fallback":is_fallback}

graph = StateGraph(BasicChatState)

graph.add_node("agency_check", agency_check) 
graph.add_node("llm_decision", llm_decision)
graph.add_node("retrieve", retrieve)
graph.add_node("general_chat",general_chat)
graph.add_node("generate", generate_response) 
graph.add_node("other", other_response)
graph.add_node("rewrite_query", rewrite_query)

graph.set_entry_point("rewrite_query")
graph.add_edge("rewrite_query", "agency_check")
graph.add_edge("agency_check", "llm_decision")

graph.add_conditional_edges(
    "llm_decision",
    get_route,
    {
        "retrieve" : "retrieve",
        "general" : "general_chat",
        "other": "other"
    }
)

graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)
graph.add_edge("general_chat",END)
graph.add_edge("other", END)

app = graph.compile(checkpointer=memory)

#ส่วนนี้อาจจะต้องเปลี่ยนไปตาม session id ของผู้ใช้อาจจะต้องมาปรับแก้อีกทีในตอนเข้า api endpoint
# config = {"configurable": {
#     "thread_id": 1
# }}

def chat_rag_memory(message,embedder,user_id):
    config = {"configurable": {
        "thread_id": user_id, 
        "embedding_model": embedder
    }}
    res = app.invoke({
        "messages": HumanMessage(content=message),
        "is_fallback": False
    }, config=config)
    print("---------------------------------------")

    response = {
        "user_message": message,
        "rewritten_question": res["rewritten_question"], #เพิ่มฟิลด์ลง dbด้วย
        "ai_message": res["messages"][-1].content,
        "question_agency": res["agency"],
        "route_decision": res["route_decision"], #เพิ่มฟิลด์ลง dbด้วย
        "is_fallback": res["is_fallback"],
    }
    print(response)
    return response


# answer = chat_rag_memory("คุณสมบัติของผู้กู้ยืมกยศ.มีกี่ลักษณะ",vector_store_from_client,"test_user_123")

# answer = chat_rag_memory("ขอรายละเอียดลักษณะที่2",vector_store_from_client,"test_user_123")

# answer = chat_rag_memory("ขอลักษณะที่3ด้วย",vector_store_from_client,"test_user_123")

# answer = chat_rag_memory("ลักษณะที่1ด้วย",vector_store_from_client,"test_user_123")

# answer = chat_rag_memory("ต้องการลงทะเบียนเรียนล่าช้าต้องทำไง",vector_store_from_client,"test_user_123")

# answer = chat_rag_memory("เมื่อกี้ฉันถามอะไรไปบ้าง",vector_store_from_client,"test_user_123")

# answer = chat_rag_memory("สวัสดี นายชื่อไร",vector_store_from_client,"test_user_123")

# answer = chat_rag_memory("อยากเป็นโจรสลัด",vector_store_from_client,"test_user_123")

# answer = chat_rag_memory("เข้าสู่ระบบ suit accountไม่ได้",vector_store_from_client,"test_user_123")

# เอาrewriteไปรันพร้อม api แก้ข้อมูลเข้าออกด้วย