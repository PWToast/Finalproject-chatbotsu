# โปรเจค: การพัฒนาแชทบอทสำหรับตอบคำถามที่พบบ่อยในมหาวิทยาลัยศิลปากร โดยใช้เทคนิคการสร้างข้อความโดยมีการเสริมด้วยการค้นคืนข้อมูล

![image alt](https://github.com/PWToast/Finalproject_SU-Chatbot-FAQ/blob/a0ef45717a22aab8b79efc1b0243f7b2eaf2ba09/SU%20Chatbot%20FAQ%20-%20Tech%20Stack.jpg)

## Features
## ผู้ใช้ทั่วไป 
- ล็อคอิน, สมัครบัญชี
- สร้างห้อง, ลบห้อง, เลือกห้องที่ต้องการเพื่อคุยกับ Ai
- สนทนากับ Ai
## ผู้ดูแลระบบ
- DashBoard
- เพิ่มข้อมูลลง VectorDB
- จัดการข้อมูล VectorDB, ลบข้อมูลเอกสาร VectorDB
- ตรวจสอบประวัติการสนทนา
- จัดการแก้ไข prompt
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
MYSQL_URL_3307=mysql+pymysql://user1:mysql123456@localhost:3307/my_db

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
