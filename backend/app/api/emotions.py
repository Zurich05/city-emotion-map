from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.response import success
from app.database.session import get_db
from app.models.cleaned_post import CleanedPost
from app.models.raw_post import RawPost
from app.models.sentiment_result import SentimentResult

router = APIRouter(prefix="/api", tags=["emotions"])


@router.get("/emotions")
def list_emotions(platform: str | None = None, city: str | None = None, district: str | None = None, emotion_type: str | None = Query(None), db: Session = Depends(get_db)):
    query = db.query(CleanedPost, RawPost, SentimentResult).join(RawPost, CleanedPost.raw_id == RawPost.id).join(SentimentResult, SentimentResult.post_id == CleanedPost.id)
    if platform:
        query = query.filter(RawPost.platform == platform)
    if city:
        query = query.filter(CleanedPost.city == city)
    if district:
        query = query.filter(CleanedPost.district == district)
    if emotion_type in {"positive", "negative", "neutral"}:
        query = query.filter(SentimentResult.sentiment_label == emotion_type)
    rows = query.limit(1000).all()
    data = [
        {
            "id": cleaned.id,
            "text": cleaned.clean_text,
            "platform": raw.platform,
            "city": cleaned.city,
            "district": cleaned.district,
            "location_name": cleaned.location_name,
            "lat": cleaned.lat,
            "lng": cleaned.lng,
            "publish_time": raw.publish_time,
            "sentiment_label": sentiment.sentiment_label,
            "sentiment_score": sentiment.sentiment_score,
            "stress_score": sentiment.stress_score,
            "joy_score": sentiment.joy_score,
            "anger_score": sentiment.anger_score,
            "calm_score": sentiment.calm_score,
        }
        for cleaned, raw, sentiment in rows
    ]
    return success(data)
