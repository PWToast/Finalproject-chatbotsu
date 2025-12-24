from app.db.mysql import get_connection
from mysql.connector import Error
from datetime import datetime
def ensure_line_user(line_user_id: str) -> bool:
    """
    ถ้าไม่มี return True
    ถ้ามีอยู่แล้ว return False
    """

    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now()
    try:
        cursor.execute("""INSERT INTO line_users (line_user_id,created_at) VALUES (%s,%s)""",
            (line_user_id,timestamp)
        )
        conn.commit()
        return True

    except Error as e:

        if e.errno == 1062:
            return False
        else:
            raise e

    finally:
        cursor.close()
        conn.close()
