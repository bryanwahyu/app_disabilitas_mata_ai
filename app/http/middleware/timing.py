import time

from fastapi import FastAPI, Request


def register_timing_middleware(app: FastAPI):
    @app.middleware("http")
    async def add_process_time(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        response.headers["X-Process-Time"] = f"{duration_ms}ms"
        return response
