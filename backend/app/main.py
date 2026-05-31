from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api import audit, auth, backup, clean, crawl, emotions, health, hotspots, import_data, report, sentiment, statistics, users
from app.core.config import settings
from app.core.exceptions import AppError, app_error_handler
from app.database.init_db import init_db
from app.database.session import SessionLocal
from app.services.audit_service import is_audited_path, write_operation_log


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

    @app.middleware("http")
    async def audit_middleware(request: Request, call_next):
        response = await call_next(request)
        if is_audited_path(request.url.path):
            db = SessionLocal()
            try:
                write_operation_log(db, request, response.status_code)
            finally:
                db.close()
        return response

    for router in [health.router, auth.router, import_data.router, crawl.router, clean.router, sentiment.router, emotions.router, statistics.router, hotspots.router, report.router, audit.router, backup.router, users.router]:
        app.include_router(router)
    return app


app = create_app()
