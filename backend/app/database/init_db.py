from app.database.base import Base
from app.database.session import engine
from app.models import AreaStatistic, CleanedPost, ImportLog, RawPost, SentimentResult


def init_db() -> None:
    _ = (AreaStatistic, CleanedPost, ImportLog, RawPost, SentimentResult)
    Base.metadata.create_all(bind=engine)
