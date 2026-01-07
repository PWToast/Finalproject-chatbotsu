from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class PlatformType(str, Enum):
    web = "web"
    line = "line"

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

# ใช้ตอนรับข้อมูลสมัครสมาชิก
class UserCreate(BaseModel):
    user_id: str
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    line_user_id: Optional[str] = None
    platform: PlatformType
    role: UserRole = UserRole.user

# ใช้ตอนส่งข้อมูล User กลับไป (ไม่ส่ง Password)
class UserResponse(BaseModel):
    user_id: str
    username: Optional[str]
    email: Optional[EmailStr]
    platform: PlatformType
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True # ช่วยให้แปลงจาก SQLAlchemy Model ได้ง่ายขึ้น