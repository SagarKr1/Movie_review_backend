from fastapi import APIRouter , Depends
from pydantic import BaseModel


router = APIRouter()

@router.get('/')
def health_test():
    return {
        "message": "Health Test Public"
    }