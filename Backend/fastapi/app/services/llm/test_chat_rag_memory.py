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
from openai import OpenAI

# llm = OllamaLLM(model="scb10x/typhoon2.1-gemma3-4b")
# 
API_KEY = "sk-ec57KJniI86p7HzkmcoYP8680ldOIKP9DsEIZfoZ8SamDO2Z"


llm = OpenAI(
        api_key=API_KEY,
        base_url="https://api.opentyphoon.ai/v1"
    )
# 
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
    context: str
    old_documents: Annotated[list, add_messages]
    agency: str 
    route_decision: str
    is_fallback: bool
    original_message: str 

def get_route(state: BasicChatState):
    route = state.get("route_decision", "general")
    return route

def get_fallback_message(state: BasicChatState,history):
    print("เข้า fallback_suggest")
    # เตรียมเอกสารอ้างอิงเก่า ไว้แนะนำผู้ใช้
    old_documents = state["old_documents"][-1] if state["old_documents"] else ""
    # print("old_documents:\n",old_documents)
    system_raw, human_raw = get_final_prompt("fallback_suggest")
    system_prompt = system_raw.format(history=history,old_documents=old_documents)
    human_prompt = human_raw.format()
    # เรียกใช้ llm
    fallback_llm_response = llm.chat.completions.create(
        model="typhoon-v2.5-30b-a3b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_prompt}
        ],
        max_tokens=16384
    )
    response = fallback_llm_response.choices[0].message.content
    return response

def rewrite_query(state: BasicChatState):
    recent_messages = state["messages"][-7:-1] #เอา3ประวัติสนทนาล่าสุด ยกเว้นคำถามล่าสุด
    history = ""
    #จัดformat ให้ขึ้นต้นด้วย User:,AI:
    if recent_messages:
        for msg in recent_messages: 
            role = "User" if isinstance(msg, HumanMessage) else "AI"
            history += f"{role}: {msg.content}\n"
    recent_question = state["messages"][-1]
    user_question = recent_question.content
    #ถ้าไม่มีประวัติไม่ต้อง Rewrite
    if not history:
        return {"rewritten_question": user_question}#ใช้คำถามต้นฉบับ
    # ดึง prompt มาใช้งาน
    system_raw, human_raw = get_final_prompt("rewrite")
    system_prompt = system_raw.format(history=history)
    human_prompt = human_raw.format(user_question=user_question)
    # เรียกใช้ llm
    llm_response = llm.chat.completions.create(
        model="typhoon-v2.5-30b-a3b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_prompt}
        ],
        max_tokens=16384
    )
    rewritten_question = llm_response.choices[0].message.content
    #แทนที่ข้อความล่าสุดให้เป็นอันที่ผ่าน rewrite
    return {"messages": [HumanMessage(content=rewritten_question,id=recent_question.id)],
            "rewritten_question": rewritten_question}

def agency_check(state: BasicChatState):
    user_question = state["rewritten_question"]
    print("after rewrite: ",user_question)
    # ดึง prompt มาใช้งาน
    system_raw, human_raw = get_final_prompt("agency_check")
    system_prompt = system_raw.format()
    human_prompt = human_raw.format(user_question=user_question)
    # เรียกใช้ llm
    llm_response = llm.chat.completions.create(
        model="typhoon-v2.5-30b-a3b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_prompt}
        ],
        max_tokens=16384
    )
    result = llm_response.choices[0].message.content
    if result not in ["กองบริหารวิชาการ","สำนักดิจิทัลเทคโนโลยี","กองกิจการนักศึกษา","อื่นๆ"]:
        result = "อื่นๆ"
    return {"agency": result} 

def llm_decision(state: BasicChatState):
    recent_messages = state["messages"][-7:-1] #เอา3ประวัติสนทนาล่าสุด ยกเว้นคำถามล่าสุด    
    history = ""
    #จัดformat ให้ขึ้นต้นด้วย User:,AI:
    if recent_messages: #ถ้ามีข้อมูล
        for msg in recent_messages: 
            role = "User" if isinstance(msg, HumanMessage) else "AI"
            history += f"{role}: {msg.content}\n"

    user_question = state["rewritten_question"]
    # ดึง prompt มาใช้งาน
    system_raw, human_raw = get_final_prompt("decision")
    system_prompt = system_raw.format(history=history)
    human_prompt = human_raw.format(user_question=user_question)
    # เรียกใช้ llm
    llm_response = llm.chat.completions.create(
        model="typhoon-v2.5-30b-a3b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_prompt}
        ],
        max_tokens=16384
    )
    route = llm_response.choices[0].message.content

    if route not in ["retrieve","general"]:
        route = "general"

    return {"route_decision": route}

def retrieve(state: BasicChatState,config):
    #นำคำถามผู้ใช้ไปค้นหา
    user_query = state["rewritten_question"]
    vectordb = config.get("configurable", {}).get("vectordb")
    results = vectordb.similarity_search_with_score(
        user_query, 
        k=5
    )

    threshold = 0.50 # = 0.50 
    context = ""
    old_documents = ""

    for doc, score in results:
        # จัดเก็บเนื้อหาทั้งหมด
        old_documents += doc.page_content
        #จัดเก็บเนื้อหาที่ผ่าน threshold เข้า context
        if score <= threshold:
            context += doc.page_content + "\n-----------\n"
    
    return {"context": context, "old_documents": old_documents}

def generate_response(state: BasicChatState):
    print("RAG")
    recent_messages = state["messages"][-7:-1] #เอา3ประวัติสนทนาล่าสุด ยกเว้นคำถามล่าสุด
    history = ""
    #จัดformat ให้ขึ้นต้นด้วย User:,AI:
    if recent_messages:
        for msg in recent_messages: 
            role = "User" if isinstance(msg, HumanMessage) else "AI"
            history += f"{role}: {msg.content}\n"
    user_question = state["rewritten_question"]
    context = state["context"]
    # ดึง prompt มาใช้งาน
    system_raw, human_raw = get_final_prompt("rag")
    system_prompt = system_raw.format(context=context,history=history)
    human_prompt = human_raw.format(user_question=user_question)
    # เรียกใช้ llm
    llm_response = llm.chat.completions.create(
        model="typhoon-v2.5-30b-a3b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_prompt}
        ],
        max_tokens=16384
    )
    response = llm_response.choices[0].message.content
    fallback_message = "Unknown"
    agency = state["agency"]
    # หากไม่พบคำตอบจะใช้ fallback ในการตอบ
    is_fallback = False
    if response == fallback_message:
        agency = "อื่นๆ"
        response = get_fallback_message(state,history)
        is_fallback = True
    return {"messages": [AIMessage(content=response)],"agency": agency,
            "is_fallback":is_fallback}

def general_chat(state: BasicChatState):
    print("General")
    recent_messages = state["messages"][-7:-1] #เอา3ประวัติสนทนาล่าสุด ยกเว้นคำถามล่าสุด    
    history = ""
    #จัดformat ให้ขึ้นต้นด้วย User:,AI:
    if recent_messages:
        for msg in recent_messages: 
            role = "User" if isinstance(msg, HumanMessage) else "AI"
            history += f"{role}: {msg.content}\n"

    user_question = state["rewritten_question"]
    # ดึง prompt มาใช้งาน
    system_raw, human_raw = get_final_prompt("general")
    system_prompt = system_raw.format(history=history)
    human_prompt = human_raw.format(user_question=user_question)
    # เรียกใช้ llm
    llm_response = llm.chat.completions.create(
        model="typhoon-v2.5-30b-a3b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_prompt}
        ],
        max_tokens=16384
    )
    response = llm_response.choices[0].message.content
    agency = "อื่นๆ"
    fallback_message = "Unknown"
    # หากไม่พบคำตอบจะใช้ fallback ในการตอบ
    is_fallback = False
    if response == fallback_message:
        agency = "อื่นๆ"
        response = get_fallback_message(state,history)
        is_fallback = True
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
    print("original question: ",message)
    config = {"configurable": {
        "thread_id": user_id, 
        "vectordb": vectordb
    }}
    res = app.invoke({
        "messages": HumanMessage(content=message),
        "original_message": message,
        "is_fallback": False
    }, config=config)
    # print("---------------------------------------")

    response = {
        "user_message": message,
        "rewritten_question": res["rewritten_question"], 
        "ai_message": res["messages"][-1].content,
        "question_agency": res["agency"],
        "route_decision": res["route_decision"], 
        "is_fallback": res["is_fallback"],
    }
    print(response)
    return response