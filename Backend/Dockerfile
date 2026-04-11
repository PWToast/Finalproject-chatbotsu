# ใช้ Python version 3.12
FROM python:3.12-slim

WORKDIR /app

# ก็อปปี้ requirements.txt ติดตั้ง
COPY fastapi/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ก็อปปี้เนื้อหาทั้งหมดในโฟลเดอร์ fastapi เข้าไป
COPY fastapi/ .

# สั่งรัน uvicorn 
# อ้างอิงเป็น app.main:app เพราะ main.py อยู่ในโฟลเดอร์ app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]