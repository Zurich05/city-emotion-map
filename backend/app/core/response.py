from typing import Any


def success(data: Any = None, message: str = "success", meta: dict | None = None) -> dict:
    return {"code": 0, "message": message, "data": data, "meta": meta or {}}


def error(message: str, code: int = 400, data: Any = None, meta: dict | None = None) -> dict:
    return {"code": code, "message": message, "data": data, "meta": meta or {}}
