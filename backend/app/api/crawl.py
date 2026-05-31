from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.response import success
from app.database.session import get_db
from app.schemas.post import CrawlRequest
from app.services.crawler import get_adapter
from app.services.import_service import ImportService

router = APIRouter(prefix="/api/crawl", tags=["crawl"])


@router.post("/start")
async def start_crawl(payload: CrawlRequest, db: Session = Depends(get_db)):
    adapter = get_adapter(payload.platform)
    records = await adapter.search_posts(payload.keyword, payload.limit)
    return success(ImportService(db).import_records(records, payload.platform, "crawl"))
