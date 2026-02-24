import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from app.pkg.resp import error

logger = logging.getLogger(__name__)


def register_error_handler(app: FastAPI):
    @app.exception_handler(ValueError)
    async def value_error_handler(_request: Request, exc: ValueError):
        return error(message=str(exc), status_code=400)

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(_request: Request, exc: RequestValidationError):
        return error(message="Validasi gagal", status_code=422, details=exc.errors())

    @app.exception_handler(Exception)
    async def general_error_handler(_request: Request, exc: Exception):
        logger.exception("Unhandled error: %s", exc)
        return error(message="Terjadi kesalahan internal", status_code=500)
