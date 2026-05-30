# โปรเจค: การพัฒนาแชทบอทสำหรับตอบคำถามที่พบบ่อยในมหาวิทยาลัยศิลปากร โดยใช้เทคนิคการสร้างข้อความโดยมีการเสริมด้วยการค้นคืนข้อมูล

![image alt](https://github.com/PWToast/Finalproject_SU-Chatbot-FAQ/blob/c876a080b511d4e652a502852819b4fa148af152/SU%20Chatbot%20FAQ%20-%20Tech%20Stack.jpg)
```
Finalproject-chatbotsu-dev
    │   ReadMe.txt                      # คู่มืออธิบายโครงสร้างของโปรเจค [cite: 1]
    │
    ├───Backend                         # ส่วนประมวลผลหลังบ้าน (FastAPI) [cite: 1]
    │   │   docker-compose.yml          # ไฟล์ตั้งค่าสำหรับรัน Docker Services ทั้งหมด [cite: 2]
    │   │   Dockerfile                  # สคริปต์สำหรับสร้าง Image ของ Backend [cite: 2]
    │   │
    │   └───fastapi
    │       │   requirements.txt        # รายการ Library/Dependencies ที่ต้องใช้ใน Python [cite: 2]
    │       │
    │       └───app
    │           │   main.py             # Entry Point สำหรับรัน FastAPI Application [cite: 3]
    │           │
    │           ├───api                 # โฟลเดอร์เก็บ Endpoint (Routes) แยกตามโมดูล [cite: 3, 4]
    │           │       auth.py         # ระบบ Login และจัดการสิทธิ์ผู้ใช้งาน [cite: 4]
    │           │       edit_prompt.py  # API สำหรับรับค่าแก้ไข Prompt จากหน้าเว็บ [cite: 4]
    │           │       insert_and_delete_docs.py # API สำหรับเพิ่ม/ลบ ข้อมูลเอกสารในระบบ RAG [cite: 4]
    │           │       line_webhook.py # รับ-ส่งข้อความและจัดการเหตุการณ์จาก LINE [cite: 5]
    │           │       web_chatbot.py  # API หลักสำหรับบริการแชทบอทบนเว็บไซต์ [cite: 5]
    │           │       web_conversation.py # จัดการประวัติการสนทนาบนเว็บ [cite: 5]
    │           │       web_dashboard.py # API สำหรับดึงสถิติต่างๆ มาแสดงผลหน้าบ้าน [cite: 5]
    │           │
    │           ├───config
    │           │       prompt.py       # ไฟล์เก็บ System Prompt เริ่มต้นของระบบ AI [cite: 6]
    │           │
    │           ├───crud                # Create, Read, Update, Delete (ฟังก์ชันจัดการ DB) [cite: 6, 7]
    │           │       conversation.py # ฟังชันจัดการประวัติการแชทในฐานข้อมูล [cite: 7]
    │           │       dashboard.py    # ฟังก์ชันดึงข้อมูลสถิติและการใช้งาน [cite: 7]
    │           │       database.py     # ตั้งค่าการเชื่อมต่อฐานข้อมูลเบื้องต้น [cite: 7]
    │           │       db_manager.py   # ฟังก์ชันจัดการข้อมูลใน ChromaDB [cite: 8]
    │           │       edit_prompt.py  # ฟังชันสำหรับแก้ไขและอัปเดต Prompt [cite: 8]
    │           │       user.py         # ฟังก์ชันตรวจสอบ Userสำหรับ LINE [cite: 8]
    │           │       web_history.py  # ฟังก์ชันจัดการดึงของแต่ละ session_id ของเว็บไซต์ [cite: 8, 9]
    │           │
    │           ├───images
    │           │       line-chatbot-rich-menu.jpg # รูปภาพ Rich Menu สำหรับแสดงผลใน LINE [cite: 9]
    │           │
    │           ├───models              # นิยามโครงสร้าง Database (Database Schema) [cite: 9, 10]
    │           │       mongo_models.py # โครงสร้างข้อมูลใน MongoDB (เก็บประวัติแชท) [cite: 10]
    │           │       mysql_models.py # โครงสร้างตารางใน MySQL (เก็บข้อมูล User/Admin) [cite: 10]
    │           │
    │           ├───schemas             # นิยาม Data Validation (Pydantic Models) [cite: 10, 11]
    │           │       chat.py         # รูปแบบข้อมูลสำหรับการแชท [cite: 11]
    │           │       dashboard.py    # รูปแบบข้อมูลสำหรับ Dashboard สถิติ [cite: 11]
    │           │       node_prompt.py  # รูปแบบข้อมูลของ Prompt Node [cite: 11]
    │           │       upload.py       # รูปแบบข้อมูลสำหรับการอัปโหลดเอกสาร [cite: 12]
    │           │       user.py         # รูปแบบข้อมูลของผู้ใช้งาน [cite: 12]
    │           │
    │           └───services            # ส่วน Logic การทำงานหลัก (Business Logic) [cite: 12, 13]
    │               └───llm             # จัดการเรื่อง Large Language Model [cite: 13]
    │                   │   test_chat_rag_memory.py # โลจิกการทำงาน RAG และการจัดการความจำบอท [cite: 13]
    │                   │
    │                   └───docs-FAQ    # คลังความรู้ที่บอทใช้ในการตอบ (RAG Knowledge Base) [cite: 14]
    │                       │   รวมไฟล์ json.json [cite: 14]
    │                       ├───กองกิจการนักศึกษา   # เอกสาร FAQ หมวด กยศ. และหอพัก [cite: 14, 15]
    │                       ├───กองบริหารวิชาการ   # เอกสาร FAQ หมวด การลงทะเบียน/คำร้อง [cite: 15]
    │                       └───สำนักดิจิทัล        # เอกสาร FAQ หมวด IT Account/Internet [cite: 15]
    │
    └───Frontend                        # ส่วนติดต่อผู้ใช้ (React.js + Vite) [cite: 15, 16]
        │   Dockerfile                  # สคริปต์สำหรับสร้าง Image ของ Frontend [cite: 16]
        │
        ├───api
        │       Userapi.js              # ฟังก์ชันสำหรับส่ง Request ไปหา Backend API [cite: 16]
        │
        ├───component                   # ส่วนประกอบย่อย (Re-usable Components) [cite: 17]
        │       AdminSidebar.jsx        # เมนูด้านข้างสำหรับแอดมิน [cite: 17]
        │       ConfirmPromptModal.jsx  # ป๊อปอัพยืนยันการแก้ไข Prompt [cite: 17]
        │       HistoryChatModal.jsx    # หน้าต่างแสดงรายละเอียดแชทย้อนหลัง [cite: 17]
        │       HistoryTable.jsx        # ตารางแสดงรายการประวัติการสนทนา [cite: 18]
        │       Loginfrom.jsx           # แบบฟอร์มการเข้าสู่ระบบ [cite: 18]
        │       Navbar.jsx              # แถบเมนูด้านบน [cite: 18]
        │       OverviewStatCard.jsx    # การ์ดแสดงตัวเลขสถิติในหน้า Dashboard [cite: 18]
        │       PromptSection.jsx       # ส่วนแสดงผลและจัดการ Prompt [cite: 19]
        │       QuestionCategoryBarChart.jsx # กราฟแท่งแสดงหมวดหมู่คำถามที่พบบ่อย [cite: 19]
        │       UserSourcePieChart.jsx  # กราฟวงกลมแสดงสัดส่วนผู้ใช้งาน (Web vs LINE) [cite: 19]
        │       UserTrendLineChart.jsx  # กราฟเส้นแสดงแนวโน้มการใช้งาน [cite: 19]
        │
        ├───Page                        # หน้าหลักของเว็บไซต์ (Views) [cite: 19, 20]
        │       ChatHistoryPage.jsx     # หน้าแสดงประวัติการแชททั้งหมด [cite: 20]
        │       Chatpage.jsx            # หน้าสำหรับสนทนากับแชทบอท [cite: 20]
        │       DashboardPage.jsx       # หน้าแสดงภาพรวมสถิติ (Admin Overview) [cite: 20]
        │       EditPromptPage.jsx      # หน้าสำหรับแก้ไข Prompt ของระบบ [cite: 21]
        │       Homepage.jsx            # หน้าแรกของระบบ [cite: 21]
        │       ManageDataPage.jsx      # หน้าสำหรับจัดการข้อมูลเอกสาร (RAG) [cite: 21]
        │       Registerpage.jsx        # หน้าสมัครสมาชิก [cite: 21]
        │       ViewDocsPage.jsx        # หน้าแสดงรายการเอกสารที่มีในระบบ [cite: 22]
        │
        ├───service
        │       Auth.jsx                # จัดการการยืนยันตัวตนในฝั่ง Frontend [cite: 22]
        │
        └───src
                App.jsx                 # ไฟล์หลักที่รวม Routes และส่วนประกอบเว็บ [cite: 22, 23]
                main.jsx                # จุดเริ่มต้นการรัน React [cite: 23]
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
