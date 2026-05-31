from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.core.response import success
from app.database.session import get_db
from app.models.cleaned_post import CleanedPost
from app.models.import_log import ImportLog
from app.models.raw_post import RawPost
from app.models.sentiment_result import SentimentResult
from app.services.import_service import ImportService, parse_records

router = APIRouter(prefix="/api", tags=["import"])


@router.post("/import")
async def import_file(file: UploadFile = File(...), platform: str = Form("manual"), replace: bool = Form(False), db: Session = Depends(get_db)):
    if replace:
        db.query(SentimentResult).delete()
        db.query(CleanedPost).delete()
        db.query(RawPost).delete()
        db.commit()
    records = parse_records(file.filename or "upload.jsonl", await file.read())
    return success(ImportService(db).import_records(records, platform))


@router.post("/import/demo")
def import_demo(db: Session = Depends(get_db)):
    demo_path = Path(__file__).resolve().parents[1] / "data" / "demo_posts.jsonl"
    records = parse_records(demo_path.name, demo_path.read_bytes())
    return success(ImportService(db).import_records(records, task_type="import_demo"))


@router.get("/import/logs")
def list_logs(limit: int = 50, db: Session = Depends(get_db)):
    rows = db.query(ImportLog).order_by(ImportLog.start_time.desc()).limit(limit).all()
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
    return success(data)
