from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from sqlalchemy.orm import Session

from app.core.response import success
from app.core.security import require_auth, require_roles
from app.database.session import get_db
from app.models.cleaned_post import CleanedPost
from app.models.import_log import ImportLog
from app.models.raw_post import RawPost
from app.models.sentiment_result import SentimentResult
from app.services.import_service import ImportService, parse_records

router = APIRouter(prefix="/api", tags=["import"])


@router.post("/import")
async def import_file(file: UploadFile = File(...), platform: str = Form("manual"), replace: bool = Form(False), db: Session = Depends(get_db), _: object = Depends(require_roles("admin", "analyst"))):
    if replace:
        db.query(SentimentResult).delete()
        db.query(CleanedPost).delete()
        db.query(RawPost).delete()
        db.commit()
    records = parse_records(file.filename or "upload.jsonl", await file.read())
    return success(ImportService(db).import_records(records, platform))


@router.post("/import/demo")
def import_demo(db: Session = Depends(get_db), _: object = Depends(require_roles("admin", "analyst"))):
    demo_path = Path(__file__).resolve().parents[1] / "data" / "demo_posts.jsonl"
    records = parse_records(demo_path.name, demo_path.read_bytes())
    return success(ImportService(db).import_records(records, task_type="import_demo"))


@router.get("/import/logs")
def list_logs(
    task_type: str | None = None,
    platform: str | None = None,
    status: str | None = None,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    _: str = Depends(require_auth),
):
    query = db.query(ImportLog)
    if task_type:
        query = query.filter(ImportLog.task_type == task_type)
    if platform:
        query = query.filter(ImportLog.platform == platform)
    if status:
        query = query.filter(ImportLog.status == status)
    total = query.count()
    rows = query.order_by(ImportLog.start_time.desc()).offset(offset).limit(limit).all()
    data = [
        {
            "id": row.id,
            "task_type": row.task_type,
            "platform": row.platform,
            "keyword": row.keyword,
            "start_time": row.start_time,
            "end_time": row.end_time,
            "total_count": row.total_count,
            "success_count": row.success_count,
            "failed_count": row.failed_count,
            "status": row.status,
            "error_message": row.error_message,
        }
        for row in rows
    ]
    return success(data, meta={"total": total, "limit": limit, "offset": offset})
