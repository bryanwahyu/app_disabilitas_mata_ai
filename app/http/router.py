"""Central route setup — wires all handlers with their dependencies."""

from fastapi import FastAPI

from app.deps import Deps
from app.http.handlers import health, detection, ocr, scene, tts, camera


def register_routes(app: FastAPI, deps: Deps):
    app.include_router(health.create_router())
    app.include_router(detection.create_router(deps.detection))
    app.include_router(ocr.create_router(deps.ocr))
    app.include_router(scene.create_router(deps.scene))
    app.include_router(tts.create_router(deps.tts))
    app.include_router(camera.create_router(deps.camera))
