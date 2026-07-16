import mysql.connector as myConn
import bcrypt
import os
from dotenv import load_dotenv

# ==========================================
# LOAD ENV VARIABLES
# ==========================================

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# ==========================================
# CONNECT MYSQL SERVER
# ==========================================

try:
    connection = myConn.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        charset="utf8mb4",
    )

    cursor = connection.cursor()

    print("===================================")
    print("MySQL Server Connected")
    print("===================================")

    # ==========================================
    # CREATE DATABASE
    # ==========================================

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")

    # ==========================================
    # USE DATABASE
    # ==========================================

    cursor.execute(f"USE `{DB_NAME}`")

    # ==========================================
    # CREATE USERS TABLE
    # ==========================================

    user_table = """
    CREATE TABLE IF NOT EXISTS users(
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(500) NOT NULL,
        role ENUM('ADMIN','USER') DEFAULT 'USER'
    )
    """

    cursor.execute(user_table)
    print("Users Table Created")

    # ==========================================
    # CREATE MOVIES TABLE
    # ==========================================

    movies_table = """
    CREATE TABLE IF NOT EXISTS movies(
        id INT PRIMARY KEY AUTO_INCREMENT,
        movie_name VARCHAR(255) NOT NULL,
        description TEXT NOT NULL,
        genres JSON NOT NULL,
        director VARCHAR(255) NOT NULL,
        stars JSON NOT NULL,
        writer VARCHAR(255) NOT NULL,
        release_date DATE NOT NULL,
        poster_image TEXT NOT NULL
    )
    """

    cursor.execute(movies_table)
    print("Movies Table Created")

    # ==========================================
    # CREATE MOVIE REVIEW TABLE
    # ==========================================

    movies_review_table = """
    CREATE TABLE IF NOT EXISTS movie_reviews(
        id INT PRIMARY KEY AUTO_INCREMENT,
        movie_id INT NOT NULL,
        rating INT NOT NULL,
        review TEXT NOT NULL,
        sentiment VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (movie_id) REFERENCES movies(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    )
    """

    cursor.execute(movies_review_table)
    print("Movie Reviews Table Created")

    # ==========================================
    # CREATE ADMIN USER
    # ==========================================

    cursor.execute(
        "SELECT id FROM users WHERE email = %s",
        ("admin@gmail.com",),
    )

    admin_exists = cursor.fetchone()

    if not admin_exists:
        encrypt = bcrypt.hashpw(
            "password".encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        user_details = {
            "name": "Admin",
            "email": "admin@gmail.com",
            "password": encrypt,
            "role": "ADMIN",
        }

        insert_user = """
        INSERT INTO users(
            name,
            email,
            password,
            role
        )
        VALUES(%s,%s,%s,%s)
        """

        values = (
            user_details["name"],
            user_details["email"],
            user_details["password"],
            user_details["role"],
        )

        cursor.execute(insert_user, values)
        print("Admin User Created")
    else:
        print("Admin User Already Exists")

    connection.commit()

    print("===================================")
    print("Production DB is Ready")
    print("===================================")

except myConn.Error as err:

    print("===================================")
    print("Database Error:", err)
    print("===================================")

except Exception as e:

    print("===================================")
    print("Unexpected Error:", e)
    print("===================================")

finally:

    if "connection" in locals() and connection.is_connected():

        cursor.close()
        connection.close()

        print("===================================")
        print("MySQL Connection Closed")
        print("===================================")