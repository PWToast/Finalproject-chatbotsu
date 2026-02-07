from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List
import shutil
import os
from app.schemas.upload import FormToSend
from app.crud.db_manager import add_docs, get_all_docs, delete_docs, query_by_agency, query_by_category, query_by_text
router = APIRouter(prefix="", tags=["file_upload"])


@router.get("/filetest")
async def file_test():
    return {"message": "hello this is file_upload api test"}

@router.get("/getalldocs")
async def get_all_documents():
    data = get_all_docs()
    return {"docs":data}

@router.get("/querybyagency/{item}")
async def query_by_agency_name(item: str):
    response = query_by_agency(item)
    return {"response": response}

@router.get("/querybycategory/{item}")
async def query_by_category_name(item: str):
    response = query_by_category(item)
    return {"response": response}

@router.get("/querybytext/{item}")
async def query_by_text_field(item: str):
    response = query_by_text(item)
    return response

@router.delete("/deletedocs/{item_id}")
async def delete_docuemnt(item_id: str):
    try:
        delete_docs(item_id)
        return {"message":"delete success"}
    except Exception as e:
        raise Exception("error cannot delete",e)
    
@router.post("/textupload")
async def text_upload(form: FormToSend):
    form = {
        "content":form.content,
        "metadata":{
            "topic": form.metadata.topic,
            "category": form.metadata.category,
            "agency": form.metadata.agency,
            "source": form.metadata.source,
            "added_at": form.metadata.added_at,
        }
    }
    add_docs([form])
    print(form)
    return form

@router.post("/fileupload")
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