import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings:
    app_name = "城市情绪地图系统"
    version = "1.0.0"
    database_url = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'city_emotion.db'}")
    cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
    sentiment_provider = os.getenv("SENTIMENT_PROVIDER", "local")
    sentiment_api_key = os.getenv("SENTIMENT_API_KEY", "")
    sentiment_api_url = os.getenv("SENTIMENT_API_URL", "")
    sentiment_model_name = os.getenv("SENTIMENT_MODEL_NAME", "local-rule-v1")
    auth_username = os.getenv("AUTH_USERNAME", "admin")
    auth_password = os.getenv("AUTH_PASSWORD", "admin123")
    jwt_secret_key = os.getenv("JWT_SECRET_KEY", "change-this-secret-in-production")
    jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "720"))


settings = Settings()
