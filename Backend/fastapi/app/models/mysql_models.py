from sqlalchemy import Column, String, DateTime, Enum, func
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

# สร้าง Enum สำหรับ Platform และ Role
class PlatformType(str, enum.Enum):
    web = "web"
    line = "line"

class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = "users"
    #uuid
    user_id = Column(String(50), primary_key=True, index=True)
    
   #nullable=True ฟิลด์นั้นใส่ไม่ใส่ข้อมูลก็ได้ เพราะฟิลด์บางอันไลน์ไม่มีแต่เว็บมี
    username = Column(String(50), unique=True, index=True, nullable=True)
    email = Column(String(100), unique=True, index=True, nullable=True)
    password = Column(String(255), nullable=True)
    
    line_user_id = Column(String(100), unique=True, index=True, nullable=True)
    
    platform = Column(Enum(PlatformType), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())