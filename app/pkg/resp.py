"""Standardized response envelope matching Go backend pattern."""

from typing import Any

from fastapi.responses import JSONResponse


def success(message: str, data: Any = None, status_code: int = 200) -> JSONResponse:
    body: dict[str, Any] = {"success": True, "message": message}
    if data is not None:
        body["data"] = data
    return JSONResponse(content=body, status_code=status_code)


def error(message: str, status_code: int = 500, details: Any = None) -> JSONResponse:
    body: dict[str, Any] = {"success": False, "message": message}
    if details is not None:
        body["details"] = details
    return JSONResponse(content=body, status_code=status_code)
