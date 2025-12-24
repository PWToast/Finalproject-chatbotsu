import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="user1",
        port=3307,
        password="mysql123456",
        database="my_db",
    )
