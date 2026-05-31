from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.response import success
from app.database.session import get_db
from app.services.statistics_service import StatisticsService

router = APIRouter(prefix="/api/statistics", tags=["statistics"])


@router.get("/overview")
def overview(db: Session = Depends(get_db)):
    return success(StatisticsService(db).overview())


@router.get("/platform")
def platform(db: Session = Depends(get_db)):
    return success(StatisticsService(db).platform())


@router.get("/timeline")
def timeline(db: Session = Depends(get_db)):
    return success(StatisticsService(db).timeline())


@router.get("/district-rank")
def district_rank(db: Session = Depends(get_db)):
    return success(StatisticsService(db).district_rank())
