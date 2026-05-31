from collections import defaultdict
from typing import TYPE_CHECKING

from app.models.cleaned_post import CleanedPost
from app.models.raw_post import RawPost
from app.models.sentiment_result import SentimentResult
from app.services.statistics_service import calculate_risk_level

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def suggestion_for(location: str | None) -> str:
    text = location or ""
    if any(word in text for word in ["站", "广场", "机场", "交通"]):
        return "建议加强高峰期秩序引导，优化交通换乘提示和现场服务信息。"
    if "医院" in text:
        return "建议优化排队引导、增加候诊信息提示，并关注服务窗口压力。"
    if any(word in text for word in ["商圈", "汉街", "江汉路"]):
        return "建议加强秩序维护，改善消费动线和排队体验。"
    if any(word in text for word in ["公园", "绿道", "东湖"]):
        return "可总结正向体验，作为公共空间持续优化案例。"
    if any(word in text for word in ["大学", "学校"]):
        return "建议关注通勤、噪声、安全和校园周边秩序问题。"
    return "建议结合现场管理、信息公开和服务反馈机制进行综合治理。"


class HotspotService:
    def __init__(self, db: "Session"):
        self.db = db

    def list_hotspots(self, limit: int = 10) -> list[dict]:
        rows = self.db.query(CleanedPost, RawPost, SentimentResult).join(RawPost, CleanedPost.raw_id == RawPost.id).join(SentimentResult, SentimentResult.post_id == CleanedPost.id).all()
        groups = defaultdict(list)
        for cleaned, raw, sentiment in rows:
            groups[(cleaned.district or "未知区域", cleaned.location_name or raw.raw_location or "未知地点")].append(sentiment)
        hotspots = []
        for (district, location), values in groups.items():
            total = len(values)
            negative = sum(1 for item in values if item.sentiment_label == "negative")
            avg_stress = sum(item.stress_score for item in values) / total
            avg_joy = sum(item.joy_score for item in values) / total
            risk = calculate_risk_level(total, avg_stress, negative, total)
            hotspots.append(
                {
                    "district": district,
                    "location_name": location,
                    "total_count": total,
                    "avg_stress_score": round(avg_stress, 4),
                    "avg_joy_score": round(avg_joy, 4),
                    "risk_level": risk,
                    "main_reason": "该区域负面和压力表达相对集中。" if risk != "low" else "该区域情绪表达整体平稳或偏正向。",
                    "suggestion": suggestion_for(location),
                }
            )
        return sorted(hotspots, key=lambda item: (item["risk_level"] == "high", item["avg_stress_score"], item["total_count"]), reverse=True)[:limit]
