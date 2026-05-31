from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.response import success
from app.core.security import require_auth
from app.database.session import get_db
from app.models.operation_log import OperationLog

router = APIRouter(prefix="/api/audit", tags=["audit"])


@router.get("/logs")
def list_audit_logs(
    method: str | None = None,
    path: str | None = None,
    username: str | None = None,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    _: str = Depends(require_auth),
):
    query = db.query(OperationLog)
    if method:
        query = query.filter(OperationLog.method == method.upper())
    if path:
        query = query.filter(OperationLog.path.like(f"{path}%"))
    if username:
        query = query.filter(OperationLog.username == username)
    total = query.count()
    rows = query.order_by(OperationLog.created_at.desc()).offset(offset).limit(limit).all()
    return success(
        [
            {
                "id": row.id,
                "username": row.username,
                "method": row.method,
                "path": row.path,
                "status_code": row.status_code,
                "client_ip": row.client_ip,
                "user_agent": row.user_agent,
                "created_at": row.created_at,
            }
            for row in rows
        ],
        meta={"total": total, "limit": limit, "offset": offset},
    )
