from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings

bearer_scheme = HTTPBearer(auto_error=False)


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub": subject, "exp": expire}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def verify_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from exc
    subject = payload.get("sub")
    if not subject:
        raise HTTPException(status_code=401, detail="Invalid token subject")
    return subject


def require_auth(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)) -> str:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return verify_access_token(credentials.credentials)
