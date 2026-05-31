from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.utils.time_utils import utc_now


class AreaStatistic(Base):
    __tablename__ = "area_statistics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    city: Mapped[str | None] = mapped_column(String(64), nullable=True)
    district: Mapped[str | None] = mapped_column(String(64), nullable=True)
    time_window: Mapped[str] = mapped_column(String(32))
    platform: Mapped[str | None] = mapped_column(String(32), nullable=True)
    total_count: Mapped[int] = mapped_column(Integer, default=0)
    positive_count: Mapped[int] = mapped_column(Integer, default=0)
    negative_count: Mapped[int] = mapped_column(Integer, default=0)
    neutral_count: Mapped[int] = mapped_column(Integer, default=0)
    avg_sentiment_score: Mapped[float] = mapped_column(Float, default=0)
    avg_stress_score: Mapped[float] = mapped_column(Float, default=0)
    avg_joy_score: Mapped[float] = mapped_column(Float, default=0)
    risk_level: Mapped[str] = mapped_column(String(32), default="low")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
