from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.response import success
from app.core.security import hash_password, require_admin
from app.database.session import get_db
from app.models.user import User

router = APIRouter(prefix="/api/users", tags=["users"])


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8, max_length=128)
    role: str = Field(default="viewer", pattern="^(admin|analyst|viewer)$")


class UserUpdate(BaseModel):
    password: str | None = Field(default=None, min_length=8, max_length=128)
    role: str | None = Field(default=None, pattern="^(admin|analyst|viewer)$")
    is_active: bool | None = None


def serialize_user(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at,
    }


@router.get("")
def list_users(db: Session = Depends(get_db), _: object = Depends(require_admin)):
    return success([serialize_user(user) for user in db.query(User).order_by(User.id.asc()).all()])


@router.post("")
def create_user(payload: UserCreate, db: Session = Depends(get_db), _: object = Depends(require_admin)):
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")
    user = User(username=payload.username, password_hash=hash_password(payload.password), role=payload.role, is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return success(serialize_user(user))


@router.patch("/{user_id}")
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db), _: object = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if payload.password:
        user.password_hash = hash_password(payload.password)
    if payload.role:
        user.role = payload.role
    if payload.is_active is not None:
        user.is_active = payload.is_active
    db.commit()
    db.refresh(user)
    return success(serialize_user(user))
