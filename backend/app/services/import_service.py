import csv
import io
import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.import_log import ImportLog
from app.models.raw_post import RawPost
from app.utils.time_utils import parse_datetime, utc_now


def normalize_raw_post(record: dict, platform: str | None = None) -> dict:
    return {
        "platform": platform or record.get("platform") or "manual",
        "source_url": record.get("source_url"),
        "keyword": record.get("keyword"),
        "raw_text": record.get("raw_text") or record.get("text") or "",
        "publish_time": parse_datetime(record.get("publish_time")),
        "crawl_time": parse_datetime(record.get("crawl_time")) or utc_now(),
        "raw_location": record.get("raw_location"),
        "city": record.get("city"),
        "district": record.get("district"),
        "location_name": record.get("location_name"),
        "lat": record.get("lat"),
        "lng": record.get("lng"),
        "like_count": int(record.get("like_count") or 0),
        "comment_count": int(record.get("comment_count") or 0),
        "share_count": int(record.get("share_count") or 0),
    }


def parse_records(filename: str, content: bytes) -> list[dict]:
    suffix = Path(filename).suffix.lower()
    text = content.decode("utf-8-sig")
    if suffix == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    if suffix == ".json":
        data = json.loads(text)
        return data if isinstance(data, list) else [data]
    if suffix == ".csv":
        return list(csv.DictReader(io.StringIO(text)))
    raise ValueError("仅支持 json、jsonl、csv 文件")


class ImportService:
    def __init__(self, db: Session):
        self.db = db

    def import_records(self, records: list[dict], platform: str | None = None, task_type: str = "import") -> dict:
        start = utc_now()
        success = 0
        failed = 0
        for record in records:
            normalized = normalize_raw_post(record, platform)
            if not normalized["raw_text"]:
                failed += 1
                continue
            self.db.add(RawPost(**normalized))
            success += 1
        self.db.add(ImportLog(task_type=task_type, platform=platform, start_time=start, end_time=utc_now(), total_count=len(records), success_count=success, failed_count=failed, status="success"))
        self.db.commit()
        return {"total_count": len(records), "success_count": success, "failed_count": failed}
