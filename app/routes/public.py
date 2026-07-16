from fastapi import APIRouter , Depends
from pydantic import BaseModel

# CONTROLLER
from app.controllers.public.login import login as login_user


router = APIRouter()

# ==========================================
# LOGIN SCHEMA
# ==========================================

class LoginSchema(BaseModel):
    email: str
    password: str


@router.get('/')
def health_test():
    return {
        "message": "Health Test Public"
    }
    
@router.post('/login')
def login(data: LoginSchema):
    return login_user(
        data.email,
        data.password
    )