# 🚀 Chatbot RAG Project (Graduation Project)

ระบบแชทบอทอัจฉริยะที่ใช้เทคนิค RAG (Retrieval-Augmented Generation) พัฒนาด้วย FastAPI, Line Messaging Api React และ ChromaDB

---

## 🛠 ขั้นตอนการติดตั้งและเริ่มใช้งาน (Setup Guide)

### 1. Clone Project
Clone โปรเจคจาก GitHub ลงมาที่เครื่อง:
เปิด Terminal ใหม่
```bash
git clone <URL_GITHUB_ของคุณ>
cd <ชื่อโฟลเดอร์โปรเจค>

cd frontend
npm install
npm run dev
```

เปิด Terminal ใหม่
```bash
cd backend
docker-compose up -d
```

เปิด Terminal ใหม่
```bash
cd backend/fastapi

# สร้างและเปิดใช้งาน Virtual Environment
python -m venv .venv

# เปิด Virtual Environment
.venv\Scripts\activate

# ติดตั้ง Dependencies
pip install -r requirements.txt
```

สร้างไฟล์ .env ไว้ใน Backend/fastapi โดยมีข้อมูลดังนี้
```bash
MYSQL_URL_3306=mysql+pymysql://user1:mysql123456@localhost:3306/my_db
MYSQL_URL_3307=mysql+pymysql://user1:mysql123456@localhost:3307/my_db

MONGO_URL=mongodb://localhost:27017/

ACCESS_TOKEN=ใส่_CHANNEL_ACCESS_TOKEN_ของคุณที่นี่
CHANNEL_SECRET=ใส่_CHANNEL_SECRET_ของคุณที่นี่
```
# ฐานข้อมูล (เลือก Port ตามที่ใช้งานจริง)
# หาก 3306 ชน ให้เปลี่ยนไปใช้ 3307 ในการเชื่อมต่อ
# สำหรับ LINE Messaging API  
ACCESS_TOKEN และ CHANNEL_SECRET ไปเอาได้ที่ LINE Developers Console

```bash
cd backend/fastapi
chroma run --path app/services/llm/chroma_db --host localhost --port 4000
```

เปิด Terminal ใหม่
```bash
cd backend/fastapi
uvicorn app.main:app --reload
```
เปิด Terminal ใหม่
```bash
ngrok http --url=suzan-uneloquent-grossly.ngrok-free.dev 8000
```
