from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.config import settings
from app.core.response import success
from app.core.security import create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(payload: LoginRequest):
    if payload.username != settings.auth_username or payload.password != settings.auth_password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return success({"access_token": create_access_token(payload.username), "token_type": "bearer"})
