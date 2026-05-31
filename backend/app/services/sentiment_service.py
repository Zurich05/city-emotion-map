import json
from pathlib import Path
from typing import TYPE_CHECKING

from app.core.config import settings
from app.utils.time_utils import utc_now

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class SentimentService:
    def __init__(self, db: "Session | None" = None):
        self.db = db
        words_path = Path(__file__).resolve().parents[1] / "data" / "emotion_words.json"
        self.words = json.loads(words_path.read_text(encoding="utf-8"))

    def _score_category(self, text: str, key: str) -> float:
        words = self.words.get(key, [])
        hits = sum(1 for word in words if word in text)
        return min(1.0, hits / max(3, len(words) / 3))

    def analyze_text_sync(self, text: str) -> dict:
        positive = self._score_category(text, "positive")
        negative = self._score_category(text, "negative")
        stress = self._score_category(text, "stress")
        joy = self._score_category(text, "joy")
        anger = self._score_category(text, "anger")
        calm = self._score_category(text, "calm")
        raw_score = positive + joy * 0.5 + calm * 0.2 - negative - stress * 0.5 - anger * 0.4
        sentiment_score = max(-1.0, min(1.0, raw_score))
        if sentiment_score > 0.12:
            label = "positive"
        elif sentiment_score < -0.12:
            label = "negative"
        else:
            label = "neutral"
        summary = "文本整体较为平稳。"
        if label == "negative":
            summary = "文本表达出较明显的压力、拥挤或不满情绪。"
        elif label == "positive":
            summary = "文本表达出满意、舒适或积极体验。"
        return {
            "sentiment_label": label,
            "sentiment_score": round(sentiment_score, 4),
            "stress_score": round(stress, 4),
            "joy_score": round(joy, 4),
            "anger_score": round(anger, 4),
            "calm_score": round(calm, 4),
            "summary": summary,
            "model_name": settings.sentiment_model_name,
            "model_version": "1.0",
        }

    async def analyze_text(self, text: str) -> dict:
        if settings.sentiment_provider != "api":
            return self.analyze_text_sync(text)
        if not settings.sentiment_api_url:
            return self.analyze_text_sync(text)
        import httpx

        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                settings.sentiment_api_url,
                headers={"Authorization": f"Bearer {settings.sentiment_api_key}"},
                json={"text": text, "model": settings.sentiment_model_name},
            )
            response.raise_for_status()
            return response.json()

    async def analyze_pending_posts(self, limit: int = 100) -> dict:
        if self.db is None:
            raise ValueError("database session is required")
        from app.models.cleaned_post import CleanedPost
        from app.models.import_log import ImportLog
        from app.models.sentiment_result import SentimentResult

        start = utc_now()
        posts = (
            self.db.query(CleanedPost)
            .outerjoin(SentimentResult, CleanedPost.id == SentimentResult.post_id)
            .filter(SentimentResult.id.is_(None))
            .limit(limit)
            .all()
        )
        success = 0
        for post in posts:
            result = await self.analyze_text(post.clean_text)
            self.db.add(
                SentimentResult(
                    post_id=post.id,
                    sentiment_label=result["sentiment_label"],
                    sentiment_score=result["sentiment_score"],
                    stress_score=result["stress_score"],
                    joy_score=result["joy_score"],
                    anger_score=result["anger_score"],
                    calm_score=result["calm_score"],
                    model_name=result.get("model_name", settings.sentiment_model_name),
                    model_version=result.get("model_version", "1.0"),
                    summary=result.get("summary"),
                )
            )
            success += 1
        self.db.add(ImportLog(task_type="sentiment", start_time=start, end_time=utc_now(), total_count=len(posts), success_count=success, failed_count=0, status="success"))
        self.db.commit()
        return {"total_count": len(posts), "success_count": success, "failed_count": 0}
