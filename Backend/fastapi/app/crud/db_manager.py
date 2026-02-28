from langchain_chroma import Chroma
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from uuid import uuid4
from langchain_core.documents import Document
import json
from datetime import datetime
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "..", "services", "llm", "chroma_db")
#print(f"กำลังจะเก็บข้อมูลไว้ที่: {os.path.abspath(db_path)}")

#client = chromadb.PersistentClient(path=db_path)  #ดู path folderให้ถูกต้อง
client = chromadb.HttpClient(host="localhost", port=4000)
# collection = client.get_or_create_collection("chatbot_rag_documents") #อันเก่า L2
collection = client.get_or_create_collection(
    name="rag_documents",
    metadata={"hnsw:space": "cosine"} 
)#อันใหม่ ใช้cosine
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
vector_store_from_client = Chroma(
    client=client,
    collection_name="rag_documents",
    embedding_function=embedding_model,
)

def watch_collect():
    all_collections = client.list_collections()

    print("รายการ Collection ทั้งหมดในฐานข้อมูล:")
    for col in all_collections:
        print(f"- ชื่อ: {col.name}")

# def add_docs(path,vector_store_from_client):
#     with open(path, "r", encoding="utf-8") as f:
#         data = json.load(f)

#     documents = []

#     for i,item in enumerate(data, start=1):
#         # now = datetime.now()
#         # formatted = now.strftime("%d/%m/%Y %H:%M")
#         doc = Document(
#             page_content=item["content"],
#             metadata=item["metadata"]
#         )
#         documents.append(doc)

#     for doc in documents:
#         print(doc.page_content)
#         print(doc.metadata)
#         print("-"*30)

#     uuids = [str(uuid4()) for _ in range(len(documents))]
#     vector_store_from_client.add_documents(documents=documents, ids=uuids)
#     print("add completed")

def add_docs(data):
    print("test test")
    documents = []
    

    for i,item in enumerate(data, start=1):
        # now = datetime.now()
        # formatted = now.strftime("%d/%m/%Y %H:%M")
        doc = Document(
            page_content=item["content"],
            metadata=item["metadata"]
        )
        documents.append(doc)

    for doc in documents:
        print(doc.page_content)
        print(doc.metadata)
        print("-"*30)
    
    uuids = [str(uuid4()) for _ in range(len(documents))]
    vector_store_from_client.add_documents(documents=documents, ids=uuids)
    print("add completed")
    #show_all_docs()

def show_all_docs():
    print("Collection name:", collection.name)
    print("Number of documents:", collection.count())
    # print("Metadata fields:", collection.get()["metadatas"]) 

    documents = collection.get()
    for doc_id, content, metadata in zip(documents["ids"], documents["documents"], documents["metadatas"]):
        print(f"ID: {doc_id}")
        print(f"Content: {content}")
        print(f"Metadata: {metadata}")
        print("-" * 30)
    
def get_all_docs():
    results = collection.get()
    formatted_docs = []

    if results["ids"]:
        # ใช้ zip เพื่อจับคู่ id, content, metadata ของแต่ละรายการเข้าด้วยกัน
        for doc_id, content, metadata in zip(results["ids"], results["documents"], results["metadatas"]):
            formatted_docs.append({
                "id": doc_id,
                "content": content,
                "metadata": metadata
            })
    return formatted_docs

def delete_docs(uuid):
    # uuids_to_delete = [
    #     "1fd8ecfe-3b21-4899-a775-27e71f865e75"
    # ]
    # vector_store_from_client.delete(ids=uuids_to_delete)

    collection.delete(ids=[uuid])

def query_by_agency(agency_name):
    #กองบริหารวิชาการ, สำนักดิจิทัลเทคโนโลยี, กองกิจการนักศึกษา
    results = collection.get(
        where={"agency": agency_name}
    )
    formatted_docs = []
    if results["ids"]:
        for doc_id, content, metadata in zip(results["ids"], results["documents"], results["metadatas"]):
            formatted_docs.append({
                "id": doc_id,
                "content": content,
                "metadata": metadata
            })
    return formatted_docs

def query_by_category(category_name):
    #Reg, บริการคอมพิวเตอร์, กองทุนเงินให้กู้ยืมเพื่อการศึกษา, หอพัก
    results = collection.get(
        where={"category": category_name}
    )
    formatted_docs = []
    if results["ids"]:
        for doc_id, content, metadata in zip(results["ids"], results["documents"], results["metadatas"]):
            formatted_docs.append({
                "id": doc_id,
                "content": content,
                "metadata": metadata
            })
    return formatted_docs

def query_by_text(text):
    query_vector = embedding_model.embed_query(text)
    #.query กับ .get ให้ return มา format ไม่เหมือนกันเลยต้องเปลี่ยนวิธีการ mapping ก่อนจะส่งออกให้ api
    results = collection.query(
        n_results= 10,
        query_embeddings= [query_vector]
    )
    formatted_docs = []
    if results["ids"] and results["ids"][0]: 
        
        for doc_id, content, metadata in zip(results["ids"][0], results["documents"][0], results["metadatas"][0]):
            formatted_docs.append({
                "id": doc_id,
                "content": content,
                "metadata": metadata
            })
    return formatted_docs

# add_docs("docs-FAQ/กองกิจการนักศึกษา/....json",vector_store_from_client)
# delete_docs(vector_store_from_client)

