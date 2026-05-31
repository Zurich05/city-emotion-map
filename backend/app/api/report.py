from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.response import success
from app.database.session import get_db
from app.services.report_service import ReportService

router = APIRouter(prefix="/api", tags=["report"])


@router.get("/report")
def report(db: Session = Depends(get_db)):
    return success(ReportService(db).generate())
