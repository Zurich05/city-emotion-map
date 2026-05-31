from sqlalchemy.orm import Session

from app.models.cleaned_post import CleanedPost
from app.models.import_log import ImportLog
from app.models.raw_post import RawPost
from app.services.geo_service import infer_geo
from app.utils.hash import text_hash
from app.utils.privacy import mask_coordinate
from app.utils.text_cleaner import clean_text
from app.utils.time_utils import utc_now


class CleanService:
    def __init__(self, db: Session):
        self.db = db

    def run(self, limit: int = 500) -> dict:
        start = utc_now()
        rows = (
            self.db.query(RawPost)
            .outerjoin(CleanedPost, RawPost.id == CleanedPost.raw_id)
            .filter(CleanedPost.id.is_(None))
            .limit(limit)
            .all()
        )
        seen_hashes = {row.user_hash for row in self.db.query(CleanedPost.user_hash).all() if row.user_hash}
        success = 0
        failed = 0
        for raw in rows:
            cleaned = clean_text(raw.raw_text)
            digest = text_hash(cleaned)
            if not cleaned or digest in seen_hashes:
                failed += 1
                continue
            geo = infer_geo(
                {
                    "raw_location": raw.raw_location,
                    "city": getattr(raw, "city", None),
                    "district": getattr(raw, "district", None),
                    "location_name": getattr(raw, "location_name", None),
                }
            )
            self.db.add(
                CleanedPost(
                    raw_id=raw.id,
                    clean_text=cleaned,
                    city=geo["city"],
                    district=geo["district"],
                    location_name=geo["location_name"],
                    lat=mask_coordinate(getattr(raw, "lat", None)),
                    lng=mask_coordinate(getattr(raw, "lng", None)),
                    user_hash=digest,
                    clean_status="cleaned",
                )
            )
            seen_hashes.add(digest)
            success += 1
        self.db.add(ImportLog(task_type="clean", start_time=start, end_time=utc_now(), total_count=len(rows), success_count=success, failed_count=failed, status="success"))
        self.db.commit()
        return {"total_count": len(rows), "success_count": success, "failed_count": failed}
