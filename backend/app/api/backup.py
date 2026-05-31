import json

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.security import require_auth
from app.database.session import get_db
from app.models.cleaned_post import CleanedPost
from app.models.import_log import ImportLog
from app.models.raw_post import RawPost
from app.models.sentiment_result import SentimentResult
from app.utils.time_utils import parse_datetime

router = APIRouter(prefix="/api/backup", tags=["backup"])


def serialize_row(row) -> dict:
    data = {}
    for column in row.__table__.columns:
        value = getattr(row, column.name)
        data[column.name] = value.isoformat() if hasattr(value, "isoformat") else value
    return data


def parse_datetime_fields(table_model, row: dict) -> dict:
    parsed = dict(row)
    for column in table_model.__table__.columns:
        if column.type.__class__.__name__ == "DateTime" and parsed.get(column.name):
            parsed[column.name] = parse_datetime(parsed[column.name])
    return parsed


@router.get("/export")
def export_backup(db: Session = Depends(get_db), _: str = Depends(require_auth)):
    payload = {
        "raw_posts": [serialize_row(row) for row in db.query(RawPost).all()],
        "cleaned_posts": [serialize_row(row) for row in db.query(CleanedPost).all()],
        "sentiment_results": [serialize_row(row) for row in db.query(SentimentResult).all()],
        "import_logs": [serialize_row(row) for row in db.query(ImportLog).all()],
    }
    return JSONResponse(content=payload, media_type="application/json", headers={"Content-Disposition": 'attachment; filename="city-emotion-backup.json"'})


@router.post("/restore")
async def restore_backup(file: UploadFile = File(...), replace: bool = Form(False), db: Session = Depends(get_db), _: str = Depends(require_auth)):
    payload = json.loads((await file.read()).decode("utf-8-sig"))
    if replace:
        db.query(SentimentResult).delete()
        db.query(CleanedPost).delete()
        db.query(RawPost).delete()
        db.query(ImportLog).delete()
        db.commit()

    counts = {"raw_posts": 0, "cleaned_posts": 0, "sentiment_results": 0, "import_logs": 0}
    for row in payload.get("raw_posts", []):
        db.merge(RawPost(**parse_datetime_fields(RawPost, row)))
        counts["raw_posts"] += 1
    for row in payload.get("cleaned_posts", []):
        db.merge(CleanedPost(**parse_datetime_fields(CleanedPost, row)))
        counts["cleaned_posts"] += 1
    for row in payload.get("sentiment_results", []):
        db.merge(SentimentResult(**parse_datetime_fields(SentimentResult, row)))
        counts["sentiment_results"] += 1
    for row in payload.get("import_logs", []):
        db.merge(ImportLog(**parse_datetime_fields(ImportLog, row)))
        counts["import_logs"] += 1
    db.commit()
    return {"code": 0, "message": "success", "data": counts, "meta": {}}
