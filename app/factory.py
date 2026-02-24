"""Application factory — wires all dependencies and creates FastAPI app."""

from fastapi import FastAPI

from app.config.config import Config, load_config
from app.deps import Deps
from app.domain.detection.repository import MobileNetRepository
from app.domain.detection.service import DetectionService
from app.domain.ocr.repository import TesseractRepository
from app.domain.ocr.service import OCRService
from app.domain.scene.repository import BLIPRepository
from app.domain.scene.service import SceneService
from app.domain.tts.repository import GTTSRepository
from app.domain.tts.service import TTSService
from app.domain.camera.service import CameraService
from app.infra.translator import TranslatorService
from app.http.router import register_routes
from app.http.middleware.error_handler import register_error_handler
from app.http.middleware.timing import register_timing_middleware


def create_app(config: Config | None = None) -> FastAPI:
    if config is None:
        config = load_config()

    app = FastAPI(
        title=config.app.name,
        description=config.app.description,
        version=config.app.version,
    )

    # Infrastructure
    translator = TranslatorService(config.models.translator)

    # Repositories (AI model wrappers)
    detection_repo = MobileNetRepository(config.models.detection)
    ocr_repo = TesseractRepository(config.models.ocr)
    scene_repo = BLIPRepository(config.models.scene)
    tts_repo = GTTSRepository(config.models.tts)

    # Domain services
    detection_svc = DetectionService(detection_repo)
    ocr_svc = OCRService(ocr_repo)
    scene_svc = SceneService(scene_repo, translator)
    tts_svc = TTSService(tts_repo)
    camera_svc = CameraService(detection_svc, config.camera)

    deps = Deps(
        config=config,
        detection=detection_svc,
        ocr=ocr_svc,
        scene=scene_svc,
        tts=tts_svc,
        camera=camera_svc,
        translator=translator,
    )

    # Middleware
    register_timing_middleware(app)
    register_error_handler(app)

    # Routes
    register_routes(app, deps)

    return app
