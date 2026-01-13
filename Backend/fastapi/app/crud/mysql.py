import mysql.connector

def get_connection():
    return mysql.connector.connect(#เชื่อม db ที่เก็บ line_users, web_users
        host="localhost",
        user="user1",
        port=3307,
        password="mysql123456",
        database="my_db",
    )
