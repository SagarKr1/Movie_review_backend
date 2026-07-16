from fastapi import Header, HTTPException
from jose import jwt, JWTError

from dotenv import load_dotenv
import os

# ==========================================
# LOAD ENV VARIABLES
# ==========================================

load_dotenv()

SECRET_KEY = os.getenv("AUTH_SECRET")
ALGORITHM = os.getenv("ALGORITHM")

# ==========================================
# VERIFY JWT TOKEN
# ==========================================

def verify_token(
    authorization: str = Header(None)
):

    if not authorization:

        raise HTTPException(
            status_code=401,
            detail="Authorization Token Missing"
        )

    try:

        # REMOVE 'Bearer '
        token = authorization.split(" ")[1]

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Token Parsing Failed"
        )

# ==========================================
# ADMIN AUTH
# ==========================================

def admin_auth(
    authorization: str = Header(None)
):

    payload = verify_token(authorization)

    if payload.get("role") != "ADMIN":

        raise HTTPException(
            status_code=403,
            detail="Admin Access Required"
        )

    return payload