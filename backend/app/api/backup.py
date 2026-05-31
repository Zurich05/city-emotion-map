from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.security import require_auth
from app.database.session import get_db
from app.models.cleaned_post import CleanedPost
from app.models.import_log import ImportLog
from app.models.raw_post import RawPost
from app.models.sentiment_result import SentimentResult

router = APIRouter(prefix="/api/backup", tags=["backup"])


def serialize_row(row) -> dict:
    data = {}
    for column in row.__table__.columns:
        value = getattr(row, column.name)
        data[column.name] = value.isoformat() if hasattr(value, "isoformat") else value
    return data


@router.get("/export")
def export_backup(db: Session = Depends(get_db), _: str = Depends(require_auth)):
    payload = {
        "raw_posts": [serialize_row(row) for row in db.query(RawPost).all()],
        "cleaned_posts": [serialize_row(row) for row in db.query(CleanedPost).all()],
        "sentiment_results": [serialize_row(row) for row in db.query(SentimentResult).all()],
        "import_logs": [serialize_row(row) for row in db.query(ImportLog).all()],
    }
    return JSONResponse(content=payload, media_type="application/json", headers={"Content-Disposition": 'attachment; filename="city-emotion-backup.json"'})
