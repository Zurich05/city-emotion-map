from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.response import success
from app.core.security import require_auth
from app.database.session import get_db
from app.services.sentiment_service import SentimentService

router = APIRouter(prefix="/api/sentiment", tags=["sentiment"])


@router.post("/run")
async def run_sentiment(db: Session = Depends(get_db), _: str = Depends(require_auth)):
    return success(await SentimentService(db).analyze_pending_posts())
