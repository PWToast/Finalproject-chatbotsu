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
llm = OpenAI(
        api_key="sk-ec57KJniI86p7HzkmcoYP8680ldOIKP9DsEIZfoZ8SamDO2Z",
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
    documents: list
    old_documents: Annotated[list, add_messages]
    agency: str 
    route_decision: str
    is_fallback: bool
    original_message: str 

def get_route(state: BasicChatState):
    route = state.get("route_decision", "general")
    return route

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
        print("ไม่พบประวัติสนทนา ไม่ต้อง rewrite")
        #ไม่ต้องอัปเดตอะไร
        return {"rewritten_question": user_question}#ใช้คำถามต้นฉบับ
    
    # print(f"format ประวัติสนทนา:\n{history}")
    system_raw, human_raw = get_final_prompt("rewrite")
    system_prompt = system_raw.format(history=history)
    human_prompt = human_raw.format(user_question=user_question)
    # print("---rewrite---")
    # print(f"system_prompt:\n{system_prompt}")
    # print(f"human_prompt:\n{human_prompt}")
    llm_response = llm.chat.completions.create(
        model="typhoon-v2.5-30b-a3b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_prompt}
        ],
        max_tokens=16384
    )

    rewritten_question = llm_response.choices[0].message.content
    # print("คำถามต้นฉบับ: ",user_question)
    print("คำถามที่ rewrite: ",rewritten_question)
    #แทนที่คำถามล่าสุดให้เป็นอันที่ rewrite
    return {"messages": [HumanMessage(content=rewritten_question,id=recent_question.id)],
            "rewritten_question": rewritten_question}

def agency_check(state: BasicChatState):
    user_question = state["rewritten_question"]
    
    system_raw, human_raw = get_final_prompt("agency_check")
    system_prompt = system_raw.format()
    human_prompt = human_raw.format(user_question=user_question)
    # print("---agency---")
    # print(f"system_prompt:\n{system_prompt}")
    # print(f"human_prompt:\n{human_prompt}")
    llm_response = llm.chat.completions.create(
        model="typhoon-v2.5-30b-a3b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_prompt}
        ],
        max_tokens=16384
    )
    result = llm_response.choices[0].message.content
    # print("agency_check_prompt: ",agency_check_prompt)

    # result =  llm.invoke(agency_check_prompt).strip()
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

    # print("history", history)
    user_question = state["rewritten_question"]
    system_raw, human_raw = get_final_prompt("decision")
    system_prompt = system_raw.format(history=history)
    human_prompt = human_raw.format(user_question=user_question)
    # print("---decision---")
    # print(f"system_prompt:\n{system_prompt}")
    # print(f"human_prompt:\n{human_prompt}")

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
        # print("not in any route")
        route = "general"
    # print('ตัดสินใจ: ', route)
    return {"route_decision": route}

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

    threshold = 0.50 # = 0.50
    # print("เนื้อหาที่ได้จากvectorDB:")
    context = ""
    old_documents = ""
    for doc, score in state["documents"]:
        # print(f"\n{doc.page_content}")
        print(f"score (Distance): {score:.4f}")
        # print("-" * 20)
        old_documents += doc.page_content + "\n-----------\n"
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
    # print("---RAG---")
    # print(f"system_prompt:\n{system_prompt}")
    # print(f"human_prompt:\n{human_prompt}")
    llm_response = llm.chat.completions.create(
        model="typhoon-v2.5-30b-a3b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_prompt}
        ],
        max_tokens=16384
    )

    response = llm_response.choices[0].message.content
    # print("คำตอบที่ได้จาก LLM:\n",response)
    fallback_message = "Unknown"
    agency = state["agency"]
    is_fallback = False
    if response == fallback_message:
        agency = "อื่นๆ"
        # response = "ขออภัยครับ ผมยังไม่มีข้อมูลในส่วนนี้ คุณสามารถลองสอบถามเรื่อง การลงทะเบียน, เพิ่ม-ถอน, บริการคอมพิวเตอร์, กยศ. หรือเรื่องหอพัก แทนได้ครับ สนใจหัวข้อไหนเป็นพิเศษไหมครับ?"
        is_fallback = True
        print("เข้า fallback_suggest rag")
        old_documents = state["old_documents"][-1] if state["old_documents"] else ""
        print("old_documents:",old_documents)
        system_raw, human_raw = get_final_prompt("fallback_suggest")
        system_prompt = system_raw.format(history=history,old_documents=old_documents)
        human_prompt = human_raw.format()
        
        fallback_llm_response = llm.chat.completions.create(
            model="typhoon-v2.5-30b-a3b-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": human_prompt}
            ],
            max_tokens=16384
        )

        response = fallback_llm_response.choices[0].message.content
    # print("หมวดปัจจุบัน: ", agency)
    # print(f"คำตอบสุดท้าย:\n{response}\n")
    return {"messages": [AIMessage(content=response)],"agency": agency,"is_fallback":is_fallback, "old_documents": old_documents}

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
    # print("---general---")
    # print(f"system_prompt:\n{system_prompt}")
    # print(f"human_prompt:\n{human_prompt}")
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
    is_fallback = False
    if response == fallback_message:
        agency = "อื่นๆ"
        #response = "ขออภัยครับ ผมยังไม่มีข้อมูลในส่วนนี้ คุณสามารถลองสอบถามเรื่อง การลงทะเบียน, เพิ่ม-ถอน, บริการคอมพิวเตอร์, กยศ. หรือเรื่องหอพัก แทนได้นะครับ หากมีข้อสงสัยอื่นเพิ่มเติม พิมพ์ถามใหม่ได้เลยครับ"
        is_fallback = True
        print("เข้า fallback_suggest general")
        system_raw, human_raw = get_final_prompt("fallback_suggest")
        old_documents = state["old_documents"][-1] if state["old_documents"] else ""
        print("old_documents:",old_documents)
        system_prompt = system_raw.format(history=history,old_documents=old_documents)
        human_prompt = human_raw.format()
        
        fallback_llm_response = llm.chat.completions.create(
            model="typhoon-v2.5-30b-a3b-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": human_prompt}
            ],
            max_tokens=16384
        )

        response = fallback_llm_response.choices[0].message.content
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