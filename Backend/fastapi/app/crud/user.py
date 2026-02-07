from app.models.mysql_models import User
from .database import SessionLocal

def is_new_line_user(line_user_id: str):
    try:
        db = SessionLocal()
        check_line_duplicated = db.query(User).filter(User.line_user_id == line_user_id).first()
        if check_line_duplicated:
            return False
                
        new_user = User(line_user_id=line_user_id, platform="line",role="user")
        db.add(new_user)
        db.commit()
        return True
    except Exception as e:
        db.rollback() # ถ้ามี Error ให้ยกเลิกสิ่งที่ทำค้างไว้
        print(f"Error: {e}")
        return False
    finally:
        db.close()


