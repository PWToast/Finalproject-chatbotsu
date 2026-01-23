from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import List
import shutil
import os

router = APIRouter(prefix="", tags=["file_upload"])

@router.get("/filetest")
async def file_test():
    return {"message": "hello this is file_upload api test"}

@router.post("/upload")
#ในฟังก์ชัน upload_file ตรง fileupload: UploadFile คำว่า "fileupload" คือ key และต้องใส่ชื่อให้ตรงตอนส่ง request หรือยิง api
async def upload_files(fileupload: List[UploadFile]):
    upload_dir = "uploads"
    #ถ้ายังไม่มีโฟลเดอร์ชื่อ uoloads มันจะสร้างขึ้นมา
    os.makedirs(upload_dir, exist_ok=True)

    saved_files = []

    #อนุญาตให้อัพโหลดเฉพาะไฟล์ pdf และ text เท่านั้น
    for file in fileupload:
        if file.content_type not in ["application/pdf", "text/plain"]:
            raise HTTPException(status_code = 422, detail = "allow only pdf and txt")

        file_location = os.path.join(upload_dir, file.filename)

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        saved_files.append({
                "file_name": file.filename,
                "content_type": file.content_type
            })
    
    return {
        "message": "All files uploaded successfully!",
        "data": saved_files
    }