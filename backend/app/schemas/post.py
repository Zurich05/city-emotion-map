from datetime import datetime

from pydantic import BaseModel


class CrawlRequest(BaseModel):
    platform: str = "mock"
    keyword: str = "地铁"
    limit: int = 50


class EmotionPoint(BaseModel):
    id: int
    text: str
    platform: str
    city: str | None = None
    district: str | None = None
    location_name: str | None = None
    lat: float | None = None
    lng: float | None = None
    publish_time: datetime | None = None
    sentiment_label: str
    sentiment_score: float
    stress_score: float
    joy_score: float
    anger_score: float
    calm_score: float
