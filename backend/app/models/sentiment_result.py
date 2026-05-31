from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.utils.time_utils import utc_now


class SentimentResult(Base):
    __tablename__ = "sentiment_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("cleaned_posts.id"), unique=True, index=True)
    sentiment_label: Mapped[str] = mapped_column(String(32), index=True)
    sentiment_score: Mapped[float] = mapped_column(Float)
    stress_score: Mapped[float] = mapped_column(Float)
    joy_score: Mapped[float] = mapped_column(Float)
    anger_score: Mapped[float] = mapped_column(Float)
    calm_score: Mapped[float] = mapped_column(Float)
    model_name: Mapped[str] = mapped_column(String(128))
    model_version: Mapped[str] = mapped_column(String(64))
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    analyzed_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    post = relationship("CleanedPost", back_populates="sentiment")
