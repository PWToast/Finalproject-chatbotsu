
from app.db.dashboard_mysql_query import get_users_count
from app.db.dashboard_mongodb_query import get_conversation_count
from pydantic import BaseModel

class DashboardOverview(BaseModel):
    total_users: int
    total_conversations: int

#ภาพรวม
#นับผู้ใช้สะสม
#นับจำนวนบทสนทนาสะสม
#นับจำนวนคำถามที่ตอบได้
#นับจำนวนคำถามที่ตอบไม่ได้
def overview_count():
    line_users_count = get_users_count("line_users")
    web_users_count = get_users_count("web_users")
    # print("total users: ",total_users)
    line_conversation_count = get_conversation_count("line_conversation")
    web_conversation_count = get_conversation_count("web_conversation")
    total_conversation = line_conversation_count+web_conversation_count
    # print("total users: ",total_users)

    #ยังเหลือข้อมูล ตอบได้กับ ตอบไม่ได้

    return  {"line_users_count": line_users_count,"web_users_count": web_users_count, "total_conversation": total_conversation}