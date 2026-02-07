# how to install

--- นัด ---
หมายเหตุ: มีการเปลี่ยน port ตัวแรกจาก 3306 เป็น3307 ในไฟล์ docker-compose.yml
มีการเพิ่ม port:3307 และเปลี่ยน user เป็น 'user1' ในไฟล์ index.js

how to install ครั้งแรก
new terminal > cd frontend > npm install > npm run dev
new terminal > cd backend > docker compose up -d
new terminal > cd backend/fastapi > .venv\Scripts\activate > uvicorn app.main:app --reload

ครั้งต่อๆไป
new terminal > cd frontend > npm run dev
(เปิด docker desktop "backend")
new terminal > cd backend/fastapi > .venv\Scripts\activate > uvicorn app.main:app --reload

(ถ้าใช้ไลน์ด้วย) new terminal > รัน ngrok http --url=suzan-uneloquent-grossly.ngrok-free.dev 8000

admin
email: admin888@gmail.com
password: admin888
