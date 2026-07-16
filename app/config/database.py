import os
from dotenv import load_dotenv
import mysql.connector as myConn

# ==========================================
# LOAD ENV VARIABLES
# ==========================================

load_dotenv()

# ==========================================
# DATABASE CONFIG
# ==========================================

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# ==========================================
# DATABASE CONNECTION FUNCTION
# ==========================================

def get_db_connection():

    try:

        connection = myConn.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():

            print("MySQL Database Connected Successfully")

            return connection

    except myConn.Error as err:

        print("Database Connection Error:", err)

        return None