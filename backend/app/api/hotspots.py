from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.response import success
from app.database.session import get_db
from app.services.hotspot_service import HotspotService

router = APIRouter(prefix="/api", tags=["hotspots"])


@router.get("/hotspots")
def hotspots(db: Session = Depends(get_db)):
    return success(HotspotService(db).list_hotspots())
