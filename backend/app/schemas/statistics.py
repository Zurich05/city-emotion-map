from pydantic import BaseModel


class Overview(BaseModel):
    total_count: int
    today_count: int
    positive_ratio: float
    negative_ratio: float
    neutral_ratio: float
    avg_sentiment_score: float
    avg_stress_score: float
    avg_joy_score: float
    high_risk_count: int
