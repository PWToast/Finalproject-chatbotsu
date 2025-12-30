import pymongo
from pymongo.errors import PyMongoError

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["chatbot_conversation"]

def get_conversation_count(collect_name: str):
    mycol = mydb[collect_name]
    total = mycol.estimated_document_count()
    try:
        #นับรวดเดียว
        total = mycol.estimated_document_count()
        return total

    except PyMongoError as e:
        print(f"MongoDB Error: {e}")
        return 0

