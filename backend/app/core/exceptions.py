from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.response import error


class AppError(Exception):
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code


async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.code, content=error(exc.message, exc.code))
