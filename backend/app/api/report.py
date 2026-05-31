from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.response import success
from app.core.security import require_auth
from app.database.session import get_db
from app.services.report_service import ReportService

router = APIRouter(prefix="/api", tags=["report"])


@router.get("/report")
def report(db: Session = Depends(get_db)):
    return success(ReportService(db).generate())


@router.get("/report/export")
def export_report(format: str = Query("pdf", pattern="^(pdf|docx)$"), db: Session = Depends(get_db), _: str = Depends(require_auth)):
    service = ReportService(db)
    if format == "docx":
        return Response(
            content=service.export_docx(),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": 'attachment; filename="city-emotion-report.docx"'},
        )
    return Response(
        content=service.export_pdf(),
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="city-emotion-report.pdf"'},
    )
