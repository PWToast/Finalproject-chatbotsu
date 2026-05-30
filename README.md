# โปรเจค: การพัฒนาแชทบอทสำหรับตอบคำถามที่พบบ่อยในมหาวิทยาลัยศิลปากร โดยใช้เทคนิคการสร้างข้อความโดยมีการเสริมด้วยการค้นคืนข้อมูล

![image alt](https://github.com/PWToast/Finalproject_SU-Chatbot-FAQ/blob/c876a080b511d4e652a502852819b4fa148af152/SU%20Chatbot%20FAQ%20-%20Tech%20Stack.jpg)
```
Finalproject-chatbotsu-dev
    │   ReadMe.txt                      # คู่มืออธิบายโครงสร้างของโปรเจค
    │
    ├───Backend                         # ส่วนประมวลผลหลังบ้าน (FastAPI)
    │   │   docker-compose.yml          # ไฟล์ตั้งค่าสำหรับรัน Docker Services ทั้งหมด 
    │   │   Dockerfile                  # สคริปต์สำหรับสร้าง Image ของ Backend
    │   │
    │   └───fastapi
    │       │   requirements.txt        # รายการ Library/Dependencies ที่ต้องใช้ใน Python 
    │       │
    │       └───app
    │           │   main.py             # Entry Point สำหรับรัน FastAPI Application 
    │           │
    │           ├───api                 # โฟลเดอร์เก็บ Endpoint (Routes) แยกตามโมดูล 
    │           │       auth.py         # ระบบ Login และจัดการสิทธิ์ผู้ใช้งาน 
    │           │       edit_prompt.py  # API สำหรับรับค่าแก้ไข Prompt จากหน้าเว็บ 
    │           │       insert_and_delete_docs.py # API สำหรับเพิ่ม/ลบ ข้อมูลเอกสารในระบบ RAG 
    │           │       line_webhook.py # รับ-ส่งข้อความและจัดการเหตุการณ์จาก LINE 
    │           │       web_chatbot.py  # API หลักสำหรับบริการแชทบอทบนเว็บไซต์ 
    │           │       web_conversation.py # จัดการประวัติการสนทนาบนเว็บ 
    │           │       web_dashboard.py # API สำหรับดึงสถิติต่างๆ มาแสดงผลหน้าบ้าน 
    │           │
    │           ├───config
    │           │       prompt.py       # ไฟล์เก็บ System Prompt เริ่มต้นของระบบ AI 
    │           │
    │           ├───crud                # Create, Read, Update, Delete (ฟังก์ชันจัดการ DB) 
    │           │       conversation.py # ฟังชันจัดการประวัติการแชทในฐานข้อมูล 
    │           │       dashboard.py    # ฟังก์ชันดึงข้อมูลสถิติและการใช้งาน 
    │           │       database.py     # ตั้งค่าการเชื่อมต่อฐานข้อมูลเบื้องต้น 
    │           │       db_manager.py   # ฟังก์ชันจัดการข้อมูลใน ChromaDB 
    │           │       edit_prompt.py  # ฟังชันสำหรับแก้ไขและอัปเดต Prompt 
    │           │       user.py         # ฟังก์ชันตรวจสอบ Userสำหรับ LINE 
    │           │       web_history.py  # ฟังก์ชันจัดการดึงของแต่ละ session_id ของเว็บไซต์ 
    │           │
    │           ├───images
    │           │       line-chatbot-rich-menu.jpg # รูปภาพ Rich Menu สำหรับแสดงผลใน LINE 
    │           │
    │           ├───models              # นิยามโครงสร้าง Database (Database Schema) 
    │           │       mongo_models.py # โครงสร้างข้อมูลใน MongoDB (เก็บประวัติแชท) 
    │           │       mysql_models.py # โครงสร้างตารางใน MySQL (เก็บข้อมูล User/Admin)
    │           │
    │           ├───schemas             # นิยาม Data Validation (Pydantic Models) 
    │           │       chat.py         # รูปแบบข้อมูลสำหรับการแชท 
    │           │       dashboard.py    # รูปแบบข้อมูลสำหรับ Dashboard สถิติ 
    │           │       node_prompt.py  # รูปแบบข้อมูลของ Prompt Node 
    │           │       upload.py       # รูปแบบข้อมูลสำหรับการอัปโหลดเอกสาร 
    │           │       user.py         # รูปแบบข้อมูลของผู้ใช้งาน 
    │           │
    │           └───services            # ส่วน Logic การทำงานหลัก (Business Logic)
    │               └───llm             # จัดการเรื่อง Large Language Model 
    │                   │   test_chat_rag_memory.py # โลจิกการทำงาน RAG และการจัดการความจำบอท 
    │                   │
    │                   └───docs-FAQ    # คลังความรู้ที่บอทใช้ในการตอบ (RAG Knowledge Base) 
    │                       │   รวมไฟล์ json.json 
    │                       ├───กองกิจการนักศึกษา   # เอกสาร FAQ หมวด กยศ. และหอพัก 
    │                       ├───กองบริหารวิชาการ   # เอกสาร FAQ หมวด การลงทะเบียน/คำร้อง 
    │                       └───สำนักดิจิทัล        # เอกสาร FAQ หมวด IT Account/Internet 
    │
    └───Frontend                        # ส่วนติดต่อผู้ใช้ (React.js + Vite)
        │   Dockerfile                  # สคริปต์สำหรับสร้าง Image ของ Frontend 
        │
        ├───api
        │       Userapi.js              # ฟังก์ชันสำหรับส่ง Request ไปหา Backend API 
        │
        ├───component                   # ส่วนประกอบย่อย (Re-usable Components) 
        │       AdminSidebar.jsx        # เมนูด้านข้างสำหรับแอดมิน 
        │       ConfirmPromptModal.jsx  # ป๊อปอัพยืนยันการแก้ไข Prompt 
        │       HistoryChatModal.jsx    # หน้าต่างแสดงรายละเอียดแชทย้อนหลัง 
        │       HistoryTable.jsx        # ตารางแสดงรายการประวัติการสนทนา 
        │       Loginfrom.jsx           # แบบฟอร์มการเข้าสู่ระบบ 
        │       Navbar.jsx              # แถบเมนูด้านบน 
        │       OverviewStatCard.jsx    # การ์ดแสดงตัวเลขสถิติในหน้า Dashboard 
        │       PromptSection.jsx       # ส่วนแสดงผลและจัดการ Prompt 
        │       QuestionCategoryBarChart.jsx # กราฟแท่งแสดงหมวดหมู่คำถามที่พบบ่อย 
        │       UserSourcePieChart.jsx  # กราฟวงกลมแสดงสัดส่วนผู้ใช้งาน (Web vs LINE)
        │       UserTrendLineChart.jsx  # กราฟเส้นแสดงแนวโน้มการใช้งาน 
        │
        ├───Page                        # หน้าหลักของเว็บไซต์ (Views) 
        │       ChatHistoryPage.jsx     # หน้าแสดงประวัติการแชททั้งหมด 
        │       Chatpage.jsx            # หน้าสำหรับสนทนากับแชทบอท 
        │       DashboardPage.jsx       # หน้าแสดงภาพรวมสถิติ (Admin Overview) 
        │       EditPromptPage.jsx      # หน้าสำหรับแก้ไข Prompt ของระบบ 
        │       Homepage.jsx            # หน้าแรกของระบบ 
        │       ManageDataPage.jsx      # หน้าสำหรับจัดการข้อมูลเอกสาร (RAG) 
        │       Registerpage.jsx        # หน้าสมัครสมาชิก 
        │       ViewDocsPage.jsx        # หน้าแสดงรายการเอกสารที่มีในระบบ
        │
        ├───service
        │       Auth.jsx                # จัดการการยืนยันตัวตนในฝั่ง Frontend 
        │
        └───src
                App.jsx                 # ไฟล์หลักที่รวม Routes และส่วนประกอบเว็บ 
                main.jsx                # จุดเริ่มต้นการรัน React 
```
## Features
## ผู้ใช้ทั่วไป 
- ล็อคอิน, สมัครบัญชี
- สร้างห้อง, ลบห้อง และ เลือกห้องที่ต้องการเพื่อคุยกับ Ai
- สนทนากับ Ai

![SU Chatbot FAQ1](web%20screenshot/screenshot%201.png)
![SU Chatbot FAQ2](web%20screenshot/screenshot%202.png)
![SU Chatbot FAQ3](web%20screenshot/screenshot%203.png)
## ผู้ดูแลระบบ
- DashBoard
- เพิ่มข้อมูลลง VectorDB
- จัดการข้อมูล VectorDB, ลบข้อมูลเอกสาร VectorDB
- ตรวจสอบประวัติการสนทนา
- จัดการแก้ไข prompt

![SU Chatbot FAQ4](web%20screenshot/screenshot%204.png)
![SU Chatbot FAQ5](web%20screenshot/screenshot%205.png)
![SU Chatbot FAQ6](web%20screenshot/screenshot%206.png)
![SU Chatbot FAQ7](web%20screenshot/screenshot%207.png)
![SU Chatbot FAQ8](web%20screenshot/screenshot%208.png)
![SU Chatbot FAQ9](web%20screenshot/screenshot%209.png)
![SU Chatbot FAQ10](web%20screenshot/screenshot%2010.png)

---
## 🛠 ขั้นตอนการติดตั้งและเริ่มใช้งาน

Clone โปรเจคจาก GitHub ลงมาที่เครื่อง:

เปิด Terminal ใหม่
```bash
git clone https://github.com/PWToast/Finalproject-chatbotsu.git
cd Finalproject-chatbotsu
```

# สร้างไฟล์ .env ไว้ใน Backend/fastapi โดยมีข้อมูลดังนี้
```bash
MYSQL_URL_3306=mysql+pymysql://user1:mysql123456@localhost:3306/my_db
MYSQL_URL_3306=mysql+pymysql://user1:mysql123456@localhost:3307/my_db # เผื่อไว้สำหรับไม่สามารถเชื่อมต่อด้วย port 3306 ได้

MONGO_URL=mongodb://localhost:27017/

NGROK_TOKEN=ใส่_NGROK_TOKEN_ของคุณที่นี่

ACCESS_TOKEN=ใส่_CHANNEL_ACCESS_TOKEN_ของคุณที่นี่
CHANNEL_SECRET=ใส่_CHANNEL_SECRET_ของคุณที่นี่

TYPHOON_API_KEY=ใส่_TYPHOON_API_KEY_ของคุณที่นี่
```
ฐานข้อมูล (เลือก Port ตามที่ใช้งานจริง) หาก 3306 ชน ให้เปลี่ยนไปใช้ 3307 ในการเชื่อมต่อ (Backend/fastapi/app/crud/database.py)

- สำหรับ NGROK_TOKEN https://ngrok.com/ ทำการสมัครบัญชี และรับ Token ได้ที่เมนู “Your Authtoken”
- สำหรับ LINE Messaging API ACCESS_TOKEN และ CHANNEL_SECRET ไปเอาได้ที่ LINE Developers Console

- สำหรับ TYPHOON_API_KEY ในโปรเจคนี้ใช้บริการ API จาก Typhoon 
สามารถนำ API key มาใส่ที่ .env ได้ที่ https://playground.opentyphoon.ai/

# Docker

## โปรเจคนี้ใช้พื้นที่บน Docker โดยประมาณ 
10 GB (image) 
5 GB (Containers) 

เปิด Terminal ใหม่
```bash
cd backend
docker-compose up -d
```

เมื่อติดตั้งสมบูรณ์และเปิด docker สามารถเข้าใช้งานได้ที่ http://localhost:5173/
