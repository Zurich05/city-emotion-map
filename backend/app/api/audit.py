from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.response import success
from app.core.security import require_auth
from app.database.session import get_db
from app.models.operation_log import OperationLog

router = APIRouter(prefix="/api/audit", tags=["audit"])


@router.get("/logs")
def list_audit_logs(limit: int = 100, db: Session = Depends(get_db), _: str = Depends(require_auth)):
    rows = db.query(OperationLog).order_by(OperationLog.created_at.desc()).limit(limit).all()
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
        ]
    )
