from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.core.response import success
from app.database.session import get_db
from app.services.import_service import ImportService, parse_records

router = APIRouter(prefix="/api", tags=["import"])


@router.post("/import")
async def import_file(file: UploadFile = File(...), platform: str = Form("manual"), replace: bool = Form(False), db: Session = Depends(get_db)):
    if replace:
        db.execute("delete from sentiment_results")
        db.execute("delete from cleaned_posts")
        db.execute("delete from raw_posts")
    records = parse_records(file.filename or "upload.jsonl", await file.read())
    return success(ImportService(db).import_records(records, platform))
