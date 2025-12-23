# how to install

--- นัด ---
หมายเหตุ: มีการเปลี่ยน port ตัวแรกจาก 3306 เป็น3307 ในไฟล์ docker-compose.yml
มีการเพิ่ม port:3307 และเปลี่ยน user เป็น 'user1' ในไฟล์ index.js

how to install ครั้งแรก
new terminal > cd frontend > npm install > npm run dev
new terminal > cd backend > docker compose up -d
new terminal > cd backend/api > npm install > npx nodemon index.js

ครั้งต่อๆไป
new terminal > cd frontend > npm run dev
(เปิด docker desktop "backend")
new terminal > cd backend/api > npx nodemon index.js
new terminal > cd backend/llm > .venv\Scripts\activate > uvicorn test_api:app --reload

(ถ้าใช้ไลน์ด้วย) new terminal > รัน ngrok http 8000 เปลี่ยนลิ้งค์เอาลิ้งไปเปลี่ยนที่ developer console
