from fastapi import Request
from sqlalchemy.orm import Session

from app.core.security import verify_access_token
from app.models.operation_log import OperationLog


PROTECTED_PREFIXES = (
    "/api/import",
    "/api/crawl",
    "/api/clean",
    "/api/sentiment",
    "/api/report/export",
    "/api/backup",
)


def is_audited_path(path: str) -> bool:
    return path.startswith(PROTECTED_PREFIXES)


def username_from_request(request: Request) -> str | None:
    authorization = request.headers.get("authorization", "")
    if not authorization.lower().startswith("bearer "):
        return None
    token = authorization.split(" ", 1)[1]
    try:
        return verify_access_token(token)
    except Exception:
        return None


def write_operation_log(db: Session, request: Request, status_code: int) -> None:
    db.add(
        OperationLog(
            username=username_from_request(request),
            method=request.method,
            path=request.url.path,
            status_code=status_code,
            client_ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )
    )
    db.commit()
