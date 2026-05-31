from app.database.base import Base
from app.database.session import engine
from app.core.config import settings
from app.core.security import hash_password
from app.database.session import SessionLocal
from app.models import AreaStatistic, CleanedPost, ImportLog, OperationLog, RawPost, SentimentResult, User


def init_db() -> None:
    _ = (AreaStatistic, CleanedPost, ImportLog, OperationLog, RawPost, SentimentResult, User)
    Base.metadata.create_all(bind=engine)
    seed_admin_user()


def seed_admin_user() -> None:
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == settings.auth_username).first()
        if existing:
            return
        db.add(User(username=settings.auth_username, password_hash=hash_password(settings.auth_password), role="admin", is_active=True))
        db.commit()
    finally:
        db.close()
