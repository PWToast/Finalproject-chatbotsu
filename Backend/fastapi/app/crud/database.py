from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.mysql_models import Base
import os
from dotenv import load_dotenv
load_dotenv()
#DATABASE_URL = "mysql+pymysql://user1:mysql123456@localhost:3307/my_db"
#DATABASE_URL = "mysql+pymysql://user1:mysql123456@localhost:3306/my_db"
MYSQL_host_3306 = os.getenv("MYSQL_URL_3306")
MYSQL_host_3307 = os.getenv("MYSQL_URL_3307")

engine = create_engine(MYSQL_host_3306)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# สำหรับใช้กับ FastAPI (Depends)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()