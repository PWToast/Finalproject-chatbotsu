from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

file_path = 'C:/Users/pooh_/Downloads/finalproject/Backend/llm'

def listfromtxt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = lines = [line.strip() for line in file.readlines() if line.strip() != '']
    return content

data = listfromtxt("C:/Users/pooh_/Downloads/langchain project/Chroma/ลงทะเบียน.txt")

embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")


#สร้าง document
vectordb = Chroma.from_texts(
    texts=data,
    embedding=embedding_model,
    persist_directory="ลงทะเบียนchroma_db"
)

#เชื่อมต่อ document
"""vectordb = Chroma(
    persist_directory="ลงทะเบียนchroma_db",
    embedding_function=embedding_model
)"""

def retrive_document(Message):
    results = vectordb.similarity_search_with_score(
        Message, 
        k=3
    )
    return results

