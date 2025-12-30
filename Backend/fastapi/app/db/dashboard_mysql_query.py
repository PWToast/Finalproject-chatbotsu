from app.db.mysql import get_connection
from mysql.connector import Error

def get_users_count(table_name: str):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) as total FROM {table_name}")
            result = cursor.fetchone()
            return result[0]
    
    except Error as e:
        print(f"Mysql Error: {e}")
        return 0