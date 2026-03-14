from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from langchain_ollama import OllamaLLM
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.crud.edit_prompt import get_final_prompt

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
    route = state.get("route_decision", "general")
    return route

def agency_check(state: BasicChatState):
    user_question = state["rewritten_question"]

    system_raw, human_raw = get_final_prompt("agency_check")
    system_prompt = system_raw.format()
    human_prompt = human_raw.format(user_question=user_question)
    agency_check_prompt = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]
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
    system_raw, human_raw = get_final_prompt("decision")
    system_prompt = system_raw.format(history=history)
    human_prompt = human_raw.format(user_question=user_question)
    decision_prompt = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]
    # print("decision_prompt: ",decision_prompt)
    route = llm.invoke(decision_prompt).strip()
    if route not in ["retrieve","general"]:
        # print("not in any route")
        route = "general"
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
    system_raw, human_raw = get_final_prompt("rewrite")
    system_prompt = system_raw.format(history=history)
    human_prompt = human_raw.format(user_question=user_question)
    rewrite_prompt = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]
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
    vectordb = config.get("configurable", {}).get("vectordb")
    results = vectordb.similarity_search_with_score(
        user_query, 
        k=5
    )

    return {"documents": results}

def generate_response(state: BasicChatState):

    threshold = 0.35 # = 0.65
    # print("เนื้อหาที่ได้จากvectorDB:")
    context = ""
    for doc, score in state["documents"]:
        # print(f"\n{doc.page_content}")
        print(f"score (Distance): {score:.4f}")
        # print("-" * 20)
        #เก็บข้อความ
        if score <= threshold:
            context += doc.page_content + "\n-----------\n"
    print("context:", context)
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
    system_raw, human_raw = get_final_prompt("rag")
    system_prompt = system_raw.format(context=context,history=history)
    human_prompt = human_raw.format(user_question=user_question)
    rag_prompt = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]
    # print("rag_prompt: ",rag_prompt)
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
    system_raw, human_raw = get_final_prompt("general")
    system_prompt = system_raw.format(history=history)
    human_prompt = human_raw.format(user_question=user_question)
    general_prompt = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]
    # print("general_prompt: ",general_prompt)
    response = llm.invoke(general_prompt)
    agency = "อื่นๆ"
    fallback_message = "Unknown"
    is_fallback = False
    if response == fallback_message:
        response = "ขออภัยครับ ผมยังไม่มีข้อมูลในส่วนนี้ คุณสามารถลองสอบถามเรื่อง การลงทะเบียน, เพิ่ม-ถอน, บริการคอมพิวเตอร์, กยศ. หรือเรื่องหอพัก แทนได้นะครับ หากมีข้อสงสัยอื่นเพิ่มเติม พิมพ์ถามใหม่ได้เลยครับ"
        is_fallback = True
    # print("หมวดปัจจุบัน: ", agency)
    # print(f"คำตอบสุดท้าย:\n{response}\n")
    return {"messages": [AIMessage(content=response)],"agency": agency,"is_fallback":is_fallback}

graph = StateGraph(BasicChatState)

graph.add_node("rewrite_query", rewrite_query)
graph.add_node("agency_check", agency_check) 
graph.add_node("llm_decision", llm_decision)
graph.add_node("retrieve", retrieve)
graph.add_node("general_chat",general_chat)
graph.add_node("generate", generate_response) 


graph.set_entry_point("rewrite_query")
graph.add_edge("rewrite_query", "agency_check")
graph.add_edge("agency_check", "llm_decision")

graph.add_conditional_edges(
    "llm_decision",
    get_route,
    {
        "retrieve" : "retrieve",
        "general" : "general_chat",
    }
)

graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)
graph.add_edge("general_chat",END)

app = graph.compile(checkpointer=memory)

def chat_rag_memory(message,vectordb,user_id):
    config = {"configurable": {
        "thread_id": user_id, 
        "vectordb": vectordb
    }}
    res = app.invoke({
        "messages": HumanMessage(content=message),
        "is_fallback": False
    }, config=config)
    # print("---------------------------------------")

    response = {
        "user_message": message,
        "rewritten_question": res["rewritten_question"], #เพิ่มฟิลด์ลง dbด้วย
        "ai_message": res["messages"][-1].content,
        "question_agency": res["agency"],
        "route_decision": res["route_decision"], 
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