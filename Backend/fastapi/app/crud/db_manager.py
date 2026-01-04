from langchain_chroma import Chroma
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from uuid import uuid4
from langchain_core.documents import Document
import json
from datetime import datetime

client = chromadb.PersistentClient(path="app/services/llm/chroma_db")  #ดู path folderให้ถูกต้อง
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

def add_docs(path,vector_store_from_client):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

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

def delete_docs(vector_store_from_client):
    # uuids_to_delete = [
    #     "1fd8ecfe-3b21-4899-a775-27e71f865e75"
    # ]
    # vector_store_from_client.delete(ids=uuids_to_delete)

    collection.delete(where={})

# add_docs("docs-FAQ/กองกิจการนักศึกษา/....json",vector_store_from_client)
# delete_docs(vector_store_from_client)
# watch_collect()
# show_all_docs()

