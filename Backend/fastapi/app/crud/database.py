from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.mysql_models import Base

#DATABASE_URL = "mysql+pymysql://user1:mysql123456@localhost:3307/my_db"
DATABASE_URL = "mysql+pymysql://user1:mysql123456@localhost:3306/my_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# สำหรับใช้กับ FastAPI (Depends)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()