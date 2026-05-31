from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.utils.time_utils import utc_now


class CleanedPost(Base):
    __tablename__ = "cleaned_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    raw_id: Mapped[int] = mapped_column(ForeignKey("raw_posts.id"), unique=True, index=True)
    clean_text: Mapped[str] = mapped_column(Text)
    city: Mapped[str | None] = mapped_column(String(64), nullable=True)
    district: Mapped[str | None] = mapped_column(String(64), nullable=True)
    location_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    lng: Mapped[float | None] = mapped_column(Float, nullable=True)
    user_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    clean_status: Mapped[str] = mapped_column(String(32), default="cleaned")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    raw_post = relationship("RawPost", back_populates="cleaned")
    sentiment = relationship("SentimentResult", back_populates="post", uselist=False)
