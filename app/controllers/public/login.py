from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import bcrypt

from app.config.database import get_db_connection

load_dotenv()

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

@router.post("/login")
def login(email: str, password: str):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id, name, email, password, role
            FROM users
            WHERE email = %s
            """,
            (email,),
        )

        user = cursor.fetchone()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        if not bcrypt.checkpw(
            password.encode("utf-8"),
            user["password"].encode("utf-8")
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "user_id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "exp": expire,
        }

        token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return {
            "success": True,
            "message": "Login successful",
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
            },
        }
    # ==========================================
    # HTTP EXCEPTIONS
    # ==========================================

    except HTTPException as http_error:

        raise http_error

    # ==========================================
    # INTERNAL SERVER ERROR
    # ==========================================

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    # ==========================================
    # CLOSE DATABASE CONNECTION
    # ==========================================

    finally:
        cursor.close()
        connection.close()