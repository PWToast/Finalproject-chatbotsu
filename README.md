# โปรเจค: การพัฒนาแชทบอทสำหรับตอบคำถามที่พบบ่อยในมหาวิทยาลัยศิลปากร โดยใช้เทคนิคการสร้างข้อความโดยมีการเสริมด้วยการค้นคืนข้อมูล
---
## โปรเจคนี้ใช้พื้นที่บน Docker โดยประมาณ 10 GB

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

ACCESS_TOKEN=ใส่_CHANNEL_ACCESS_TOKEN_ของคุณที่นี่
CHANNEL_SECRET=ใส่_CHANNEL_SECRET_ของคุณที่นี่
```
ฐานข้อมูล (เลือก Port ตามที่ใช้งานจริง) หาก 3306 ชน ให้เปลี่ยนไปใช้ 3307 ในการเชื่อมต่อ

สำหรับ LINE Messaging API ACCESS_TOKEN และ CHANNEL_SECRET ไปเอาได้ที่ LINE Developers Console

สำหรับ ACCESS_TOKEN ในโปรเจคนี้ใช้บริการ API จาก Typhoon 
สามารถนำ API key มาใส่ที่ .env ได้ที่ https://playground.opentyphoon.ai/

# Docker

เปิด Terminal ใหม่
```bash
cd backend
docker-compose up -d
```
