from pydantic import BaseModel


class SentimentOutput(BaseModel):
    sentiment_label: str
    sentiment_score: float
    stress_score: float
    joy_score: float
    anger_score: float
    calm_score: float
    summary: str | None = None
