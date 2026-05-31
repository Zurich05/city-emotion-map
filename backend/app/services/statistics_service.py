from collections import defaultdict
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def calculate_risk_level(total_count: int, avg_stress_score: float, negative_count: int, denominator: int | None = None) -> str:
    base = denominator or total_count or 1
    negative_ratio = negative_count / base
    if total_count >= 20 and (avg_stress_score >= 0.7 or negative_ratio >= 0.6):
        return "high"
    if total_count >= 10 and avg_stress_score >= 0.45:
        return "medium"
    return "low"


class StatisticsService:
    def __init__(self, db: "Session"):
        self.db = db

    def _joined(self):
        from app.models.cleaned_post import CleanedPost
        from app.models.raw_post import RawPost
        from app.models.sentiment_result import SentimentResult

        return self.db.query(CleanedPost, RawPost, SentimentResult).join(RawPost, CleanedPost.raw_id == RawPost.id).join(SentimentResult, SentimentResult.post_id == CleanedPost.id)

    def overview(self) -> dict:
        rows = self._joined().all()
        total = len(rows)
        if not total:
            return {"total_count": 0, "today_count": 0, "positive_ratio": 0, "negative_ratio": 0, "neutral_ratio": 0, "avg_sentiment_score": 0, "avg_stress_score": 0, "avg_joy_score": 0, "high_risk_count": 0}
        labels = [r.SentimentResult.sentiment_label for r in rows]
        today_count = sum(1 for r in rows if r.RawPost.created_at.date() == date.today())
        district_rank = self.district_rank()
        high_risk_count = sum(1 for item in district_rank if item["risk_level"] == "high")
        return {
            "total_count": total,
            "today_count": today_count,
            "positive_ratio": round(labels.count("positive") / total, 4),
            "negative_ratio": round(labels.count("negative") / total, 4),
            "neutral_ratio": round(labels.count("neutral") / total, 4),
            "avg_sentiment_score": round(sum(r.SentimentResult.sentiment_score for r in rows) / total, 4),
            "avg_stress_score": round(sum(r.SentimentResult.stress_score for r in rows) / total, 4),
            "avg_joy_score": round(sum(r.SentimentResult.joy_score for r in rows) / total, 4),
            "high_risk_count": high_risk_count,
        }

    def platform(self) -> list[dict]:
        groups = defaultdict(list)
        for cleaned, raw, result in self._joined().all():
            groups[raw.platform].append(result)
        return [{"platform": key, "count": len(values), "avg_stress_score": round(sum(v.stress_score for v in values) / len(values), 4)} for key, values in groups.items()]

    def timeline(self) -> list[dict]:
        groups = defaultdict(list)
        for cleaned, raw, result in self._joined().all():
            key = (raw.publish_time or raw.created_at).strftime("%Y-%m-%d %H:00")
            groups[key].append(result)
        return [{"time": key, "count": len(values), "avg_sentiment_score": round(sum(v.sentiment_score for v in values) / len(values), 4)} for key, values in sorted(groups.items())]

    def district_rank(self) -> list[dict]:
        groups = defaultdict(list)
        for cleaned, raw, result in self._joined().all():
            groups[cleaned.district or "未知区域"].append(result)
        items = []
        for district, values in groups.items():
            total = len(values)
            negative = sum(1 for item in values if item.sentiment_label == "negative")
            avg_stress = sum(item.stress_score for item in values) / total
            items.append({"district": district, "total_count": total, "negative_ratio": round(negative / total, 4), "avg_stress_score": round(avg_stress, 4), "risk_level": calculate_risk_level(total, avg_stress, negative, total)})
        return sorted(items, key=lambda item: (item["risk_level"] == "high", item["avg_stress_score"], item["total_count"]), reverse=True)
