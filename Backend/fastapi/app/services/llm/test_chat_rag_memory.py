from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from langchain_ollama import OllamaLLM
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

llm = OllamaLLM(model="scb10x/typhoon2.1-gemma3-4b")
memory = MemorySaver()

class BasicChatState(TypedDict):
    messages: Annotated[list, add_messages]
    documents: list
    agency: str
    route_decision: str
    is_fallback: bool

def get_route(state: BasicChatState):
    route = state.get("route_decision", "other")
    return route

def agency_check(state: BasicChatState):
    question = state["messages"][-1].content
    prompt = f"""
จงพิจารณาคำถามต่อไปนี้: "{question}"

**สำคัญมาก:** ตอบเพียงตัวเลือกเดียวจากตัวเลือกต่อไปนี้ว่าอยู่ในหมวดไหน ตอบแค่ชื่อหมวดเท่านั้น

- กองบริหารวิชาการ -> ถ้าคำถามเกี่ยวกับ การลงทะเบียน เพิ่มถอนรายวิชา การยื่นขอใบคำร้องต่างๆ การใช้งานเว็บไซต์ reg ของมหาวิทยาลัยศิลปากร
- สำนักดิจิทัล -> ถ้าคำถามเกี่ยวกับ การใช้งานบริการคอมพิวเตอร์ การพิมพ์เอกสาร การใช้งาน SU-IT Account ของมหาวิทยาลัยศิลปากร
- กองกิจการนักศึกษา -> ถ้าคำถามเกี่ยวกับ กยศ(กองทุนให้กู้ยืมเพื่อการศึกษา) หอพักนักศึกษา ของมหาวิทยาลัยศิลปากร
- อื่นๆ -> **ถ้าคำถามเป็น** คำถามทั่วไป, คำถามส่วนตัว, คำถามที่เกี่ยวข้องกับการทำงานของบอท, **หรือคำถามที่ต้องการให้ทบทวนบทสนทนา เช่น 'เมื่อกี้ถามอะไรไปบ้าง'** ถ้าเข้าข่ายนี้ให้เลือก 'อื่นๆ' ทันที ไม่ว่าคำถามก่อนหน้าจะอยู่ในหมวดใดก็ตาม

"""
    # print("prompt: ",prompt)
    result =  llm.invoke(prompt).strip()
    
    
    if result not in ["กองบริหารวิชาการ","สำนักดิจิทัล","กองกิจการนักศึกษา","อื่นๆ"]:
        result = "อื่นๆ"
    
    # print('หมวด: ', result)
    return {"agency": result} 

def llm_decision(state: BasicChatState):
    all_conversation = "\n".join(msg.content for msg in state["messages"][:-1])#ยกเว้นคำถามล่าสุด
    new_question = state["messages"][-1].content

    system_msg = SystemMessagePromptTemplate.from_template(
    """คุณคือผู้เชี่ยวชาญด้านการจัดประเภทคำถามที่เกี่ยวข้องกับ การลงทะเบียน เพิ่มถอนรายวิชา การยื่นขอใบคำร้อง การใช้งานเว็บไซต์ reg 
    การใช้งานบริการคอมพิวเตอร์ การพิมพ์เอกสาร การใช้งาน SU-IT Account กยศ(กู้ยืมเพื่อการศึกษา) การเก็บชั่วโมงจิตอาสา หอพักนักศึกษา 
    คุณมีหน้าที่ตัดสินใจว่าจะส่งต่อคำถามล่าสุดไปที่ขั้นตอนใด
    
    คุณต้องตอบกลับด้วย 'คำสั่งเดียว' จากตัวเลือกต่อไปนี้เท่านั้น:
    
    1. **retrieve**: ถ้าคำถามล่าสุดเป็นคำถาม 'ใหม่' หรือ 'โดดเดี่ยว' ที่ไม่ต้องการบริบทใดๆ แต่ต้องการข้อมูลจากฐานความรู้
    2. **general**: ถ้าคำถามล่าสุดเป็นคำถาม 'ทักทาย' หรือ 'พูดคุยทั่วไป' อยู่ในขอบเขตที่เชี่ยวชาญ ซึ่งรวมถึงคำถามประเภท 'การจัดการบริบท/การทบทวนบทสนทนา' เช่น 'เมื่อกี้ถามอะไรไปบ้าง', 'คุณตอบว่าอะไรนะ'
    3. **other**: เลือกคำนี้ **ถ้าคำถามไม่เข้าข่ายทั้ง 'retrieve' และ 'general' เลย หรือ คำถามที่ไม่เกี่ยวข้องกับขอบเขตความเชี่ยวชาญ
    ---
    
    **กฎที่ต้องปฏิบัติตามอย่างเคร่งครัด:**
    * **ห้ามตอบคำถามอื่นใดนอกจากคำสั่งเดียวที่เลือกจาก 3 ตัวเลือกข้างต้น (retrieve, general, other)**
    * **ห้ามมีคำอธิบาย, เครื่องหมายวรรคตอน, หรือข้อความเพิ่มเติมใดๆ ทั้งสิ้น**
    
    ตัวอย่างการตอบที่ถูกต้อง:
    retrieve
    
    ตัวอย่างการตอบที่ถูกต้อง:
    general

    ตัวอย่างการตอบที่ถูกต้อง:
    other
    
    ---
    
    ตอนนี้จงเลือกคำสั่งที่ถูกต้องตามกฎ."""
    )
    human_msg = HumanMessagePromptTemplate.from_template(
        """บทสนทนาก่อนหน้า:
        {all_conversation}
        คำถามล่าสุด: {new_question}"""
    )

    prompt = ChatPromptTemplate.from_messages([system_msg,human_msg])
    # print("prompt: ",prompt)
    chain = prompt | llm
    # final_prompt = prompt.format(all_conversation=all_conversation,
    # new_question=new_question)
    # print("\nfinal prompt:\n", final_prompt)
    result = chain.invoke({"all_conversation": all_conversation,
    "new_question": new_question}).strip().lower()

    print("บทสนทนาก่อนหน้า: ",all_conversation)
    print("คำถามล่าสุด: ",new_question)
    print('ตัดสินใจ: ', result)
    return {"route_decision": result}

def rewrite_query(state: BasicChatState):
    all_conversation = "\n".join(msg.content for msg in state["messages"][:-1])#ยกเว้นคำถามล่าสุด
    new_question = state["messages"][-1].content

    #ถ้าไม่มีประวัติไม่ต้อง Rewrite
    if not all_conversation:
        return {"messages": state["messages"]}

    rewrite_prompt = [
        SystemMessage(content=f"""คุณคือผู้เชี่ยวชาญในการสร้าง 'คำถามภาษาไทย' ที่สมบูรณ์เพื่อใช้ค้นหาในฐานข้อมูล 
คุณต้องเข้าใจว่าผู้ใช้ต้องการจะถามอะไร โดยพิจารณาจากประวัติการสนทนาและคำถามล่าสุดของผู้ใช้ 

ประวัติการสนทนา:
{all_conversation}

**คำสั่งที่ต้องปฏิบัติตาม:** 
1.ถ้าคำถามล่าสุดสมบูรณ์อยู่แล้ว ให้ตอบคำถามเดิมไม่ต้องแก้อะไร
2.ถ้าคำถามล่าสุดมีการใช้คำหรือสรรนาม เช่น "แล้วต้อง", "ที่นั่น", "อันนั้น", "ราคาเท่าไหร่", "กี่วิชา", "กี่หน่วยกิต" หรือขาดความสมบูรณ์ของบริบท ให้สร้างคำถามใหม่ที่ทำให้รู้ว่าผู้ใช้ต้องการจะค้นหาอะไร
3.ถ้าคำถามล่าสุดไม่สมบูรณ์ ให้ตอบเฉพาะ 'คำถาม' ที่ปรับปรุงแล้วเท่านั้น ห้ามอธิบายและห้ามใส่ prefix อื่นๆ"""),
        HumanMessage(content=f"คำถามล่าสุด: {new_question}") # คำถามล่าสุดของผู้ใช้
    ]#อาจต้องกำหนดสรรพนามเพิ่ม
    # print("rewrite_prompt: ",rewrite_prompt)
    rewritten_question = llm.invoke(rewrite_prompt).strip()
    print("question: ",new_question)
    print("rewrite: ",rewritten_question)
    #แก้คำถามล่าสุดให้เป็นอันที่ rewrite
    return {"messages": state["messages"][:-1] + [HumanMessage(content=rewritten_question)]}

#Node นี้คือการดึง document จากข้อความผู้ใช้ เอาเฉพาะข้อความล่าสุดเท่านั้น
def retrieve(state: BasicChatState,config):
    
    user_query = state["messages"][-1].content
    # print("user_query at retrieve: ",user_query)
    vectordb = config.get("configurable", {}).get("embedding_model")
    results = vectordb.similarity_search_with_score(
        user_query, 
        k=3
    )

    return {"documents": results}

def generate_response(state: BasicChatState):

    
    print("เนื้อหาที่ได้จากvectorDB:")
    context = ""
    for doc, score in state["documents"]:
        print(f"\n{doc.page_content}")
        print(f"score (Distance): {score:.4f}")
        print("-" * 20)
        #เก็บข้อความ
        context += doc.page_content + "\n-----------"

    #ดึงประวัติการสนทนาทั้งหมด
    history = state["messages"][:-1] #ประวัติเก่า (ไม่รวมคำถามล่าสุด)
    latest_query = state["messages"][-1].content #คำถามล่าสุด
    # print("user_query at generate: ",latest_query)
    rag_prompt = [
        SystemMessage(content=f"""คุณเป็นผู้ช่วยของมหาวิทยาลัย ทำหน้าที่ตอบคำถามให้นักศึกษา 
        โดยใช้ข้อมูลจากเอกสารอ้างอิงที่ได้รับเท่านั้น โดยดูจากความเกี่ยวข้องกับคำถามมากที่สุด 
        ตอบเป็นภาษาที่สุภาพ เข้าใจง่าย เหมาะกับนักศึกษา 
        สามารถตอบด้วยอิโมจิได้ และสามารถลงท้ายด้วยการแนะนำเพิ่มเติมเกี่ยวกับหัวข้อคำถามนั้น
        ถ้าหากเอกสารอ้างไม่มีข้อมูลที่เกี่ยวข้องกับคำถาม ให้ตอบแค่ข้อความนี้ 'Unknown'
        ห้ามขึ้นต้นตอบด้วย "AI:" หรือ "Assistant:" หรือ prefix ใด ๆ ให้ตอบเฉพาะข้อความเท่านั้น

                      เอกสารอ้างอิง:
                      {context}"""),
        *history,
        HumanMessage(content=latest_query) # คำถามล่าสุดของผู้ใช้
    ]
    # print("rag_prompt ",rag_prompt)
    response = llm.invoke(rag_prompt)
    # print("คำตอบที่ได้จาก LLM:\n",response)
    fallback_message = "Unknown"
    agency = state["agency"]
    is_fallback = False
    if response == fallback_message:
        agency = "อื่นๆ"
        response = "ไม่พบข้อมูลที่เกี่ยวข้องในระบบ คุณสามารถถามคำถามที่เกี่ยวข้องกับ การลงทะเบียน เพิ่ม-ถอน คำร้อง บริการทางคอมพิวเตอร์ กยศ. หรือหอพักได้เป็นต้น"
        is_fallback = True
    print("หมวดปัจจุบัน: ", agency)
    print("คำตอบสุดท้าย:\n",response)
    return {"messages": [AIMessage(content=response)],"agency": agency,"is_fallback":is_fallback}

#Node นี้คือเส้นทางหากต้องการคุยทั่วไป แนะนำตัว หรือถามคำถามทั่วไป, หรือเกี่ยวกับประวัติแชท 
#ต้องถามให้รัดกุมนะรู้สึก model จะยังสับสนและแยกไม่ออกในบางที
def general_chat(state: BasicChatState):
    #ตอบคำถามทั่วไป
    history = state["messages"][:-1] # ประวัติเก่า (ไม่รวมคำถามล่าสุด)
    latest_query = state["messages"][-1].content # คำถามล่าสุด
    general_prompt = [
        SystemMessage(content=f"""คุณเป็นผู้ช่วยตอบคำถามทั่วไป ชื่อว่า SU AskMe FAQ เรียกตัวเองว่าน้องบอท คุณมีหน้าตอบคำถามผู้ใช้โดยใช้ประวัติการสนทนาอ้างอิงเท่านั้น
        ตอบเป็นภาษาที่สุภาพ เข้าใจง่าย เหมาะกับนักศึกษา สามารถตอบด้วยอิโมจิได้ ห้ามตอบข้อมูลเกี่ยวกับโมเดลและคุณไม่มีความเกี่ยวข้องกับ SCBX10
        ห้ามขึ้นต้นตอบด้วย "AI:" หรือ "Assistant:" หรือ prefix ใด ๆ ให้ตอบเฉพาะข้อความเท่านั้น"""),
        *history,
        HumanMessage(content=latest_query) # คำถามล่าสุดของผู้ใช้
    ]
    response = llm.invoke(general_prompt)
    agency = "อื่นๆ"
    print("หมวดปัจจุบัน: ", agency)
    print("คำตอบสุดท้าย:\n",response)
    return {"messages": [AIMessage(content=response)],"agency": agency}

#nodeนี้คือเส้นทางสุดท้ายถ้าหาก model เลือกไม่ถูกว่าจะตอบในเส้นทางไหน แต่พวกคำถาม คำถามทั่วไป, การสนทนาต่อเนื่อง, หรือคำถามเกี่ยวกับประวัติการสนทนา 
#ต้องถามให้รัดกุมนะรู้สึก model จะยังสับสนและแยกไม่ออกอาจทำให้หล่นในช่องนี้ได้
def other_response(state: BasicChatState):
    response = "ไม่พบข้อมูลที่เกี่ยวข้องในระบบ คุณสามารถถามคำถามที่เกี่ยวข้องกับ หอพัก, การลงทะเบียน เพิ่ม-ถอน, หรือ กยศได้เป็นต้น"
    agency = "อื่นๆ"
    is_fallback = True
    print("หมวดปัจจุบัน: ", agency)
    print("คำตอบสุดท้าย:\n",response)
    return {"messages": [AIMessage(content=response)],"agency": agency,"is_fallback":is_fallback}

graph = StateGraph(BasicChatState)

graph.add_node("agency_check", agency_check) 
graph.add_node("llm_decision", llm_decision)
graph.add_node("retrieve", retrieve)
graph.add_node("general_chat",general_chat)
graph.add_node("generate", generate_response) 
graph.add_node("other", other_response)
graph.add_node("rewrite_query", rewrite_query)

graph.set_entry_point("agency_check")
graph.add_edge("agency_check", "llm_decision")

graph.add_conditional_edges(
    "llm_decision",
    get_route,
    {
        "retrieve" : "rewrite_query",
        "general" : "general_chat",
        "other": "other"
    }
)

graph.add_edge("rewrite_query", "retrieve")
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

    return res["messages"][-1].content, res["agency"],res["is_fallback"]
