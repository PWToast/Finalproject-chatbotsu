from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter,status
from fastapi.security import OAuth2PasswordBearer
from app.models.mysql_models import User, Session_Users
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from app.schemas.user import UserCreated, UserResponse, Userlogin, LoginResponse, SessionCreated
from app.crud.database import get_db

router = APIRouter(prefix="", tags=["auth"])
#อย่าลืมเปลี่ยน port 3306 หรือ 3307ถ้ารันไม่ได้
# DATABASE_URL = "mysql+pymysql://user1:mysql123456@localhost:3307/my_db"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base.metadata.create_all(bind=engine)

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@router.post("/register", response_model=UserResponse)
async def register(item: UserCreated, db: Session = Depends(get_db)):
    #เช็คว่า email ที่รับมาจาก body ซ้ำกับใน db ไหมถ้าซ้ำ 409 conflict ไป
    check_email_duplicated = db.query(User).filter(User.email == item.email).first()
    if check_email_duplicated:
        raise HTTPException (status_code=409, detail="Email นี้ถูกใช้ไปแล้ว")
    try:
        # เอา password มาแปลงเป็น bytes เพื่อเข้ารหัสและแปลง bytes เป็น string เพื่อเก็บเข้า db
        user_data = item.model_dump()
        bytes_password = user_data["password"].encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(bytes_password,salt)
        user_data["password"] = hashed_password.decode('utf-8')

        db_user = User(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {
            "message": "register success",
            "username": db_user.username,
            "email": db_user.email
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/login", response_model=LoginResponse)
async def login(item: Userlogin, db: Session = Depends(get_db)):
    #ค้นหา user ที่ได้รับจาก body หากไม่มีให้ 401
    user = db.query(User).filter(User.email == item.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Email หรือ Password ไม่ถูกต้อง")
    
    is_password_correct = bcrypt.checkpw(
        item.password.encode('utf-8'), 
        user.password.encode('utf-8')
    )
    # หาก password ใน body และ db ไม่ตรงให้ 401
    if not is_password_correct:
        raise HTTPException(status_code=401, detail="Email หรือ Password ไม่ถูกต้อง")
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    payload ={
        "email": user.email,
        "username": user.username,
        "role": user.role,
        "exp": expire
    }
    # sign jwt ที่ใส่ email ,role,และอายุ 60นาทีเข้าไป
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    # print(f"มี.value {user.role.value}")
    return {
        "message": "login success",
        "username": user.username,
        "email": user.email,
        "role": user.role.value,
        "token": token
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="credentials ไม่ผ่าน",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Express: const token = authHeader.split(' ')[1]
        # FastAPI: oauth2_scheme ทำให้เราอัตโนมัติ เราจะได้ตัว token เพียวๆ มาเลย
        
        # Express: jwt.verify(...)
        #ถอดรหัส jwt ด้วย token ที่รับมา และ secert ที่ตั้งไว้ด้วย HS256
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        email: str = payload.get("email") # หรือ sub ตามที่คุณ set ตอน login
        role: str = payload.get("role")
        if email is None:
            raise credentials_exception
        if role is None:
            raise credentials_exception    
        # Express: req.user = user
        # FastAPI: return ค่าที่ต้องการให้ฟังก์ชันปลายทางใช้
        return {"email": email, "role": role} 
        
    except jwt.PyJWTError: # ดัก Error ของ PyJWT
        raise credentials_exception
    
def admin_required(current_user: dict = Depends(get_current_user)):
    # ตรวจสอบว่า Role ในฐานข้อมูลเป็น 'admin' หรือไม่ ใช้สำหรับแอดมิน
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: คุณไม่มีสิทธิ์เข้าถึงส่วนนี้ เฉพาะแอดมินเท่านั้น"
        )
    return current_user

@router.get("/verify")
def verify_token_route(current_user: dict = Depends(get_current_user)):
    # ตรงนี้จะทำงานได้ก็ต่อเมื่อ get_current_user ทำงานสำเร็จเท่านั้น
    # current_user คือค่าที่ return มาจาก get_current_user (เทียบเท่า req.user)
    
    email = current_user["email"]
    
    return {
        "message": f"verify success welcome, {email}",
        "role": current_user["role"]
    }

@router.post("/createsession")
def create_session(item: SessionCreated, db: Session = Depends(get_db)):
    try:
        session_data = item.model_dump()
        db_user = Session_Users(**session_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return {"message":'create session success!'}
    
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/getsession/{email}")
# ดึง email จาก token
def get_my_sessions_by_email(email: str, db: Session = Depends(get_db)):
    sessions = db.query(Session_Users).filter(Session_Users.email == email).all()
    return sessions

@router.delete("/deletesession/{session_id}")
def delete_session_by_session_id(session_id: str, db: Session = Depends(get_db)):
    selected_session = db.query(Session_Users).filter(Session_Users.session_id == session_id).first()
    if selected_session is None:
        raise HTTPException(status_code=404, detail="ไม่มี session นี้")
    db.delete(selected_session)
    db.commit()
    return {"message":"session deleted"}