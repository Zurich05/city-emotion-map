from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import clean, crawl, emotions, health, hotspots, import_data, report, sentiment, statistics
from app.core.config import settings
from app.core.exceptions import AppError, app_error_handler
from app.database.init_db import init_db


def create_app() -> FastAPI:
    init_db()
    app = FastAPI(title=settings.app_name, version=settings.version)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_exception_handler(AppError, app_error_handler)
    for router in [health.router, import_data.router, crawl.router, clean.router, sentiment.router, emotions.router, statistics.router, hotspots.router, report.router]:
        app.include_router(router)
    return app


app = create_app()
