"""Dependency container — mirrors Go Deps struct pattern."""

from dataclasses import dataclass

from app.config.config import Config
from app.domain.detection.service import DetectionService
from app.domain.ocr.service import OCRService
from app.domain.scene.service import SceneService
from app.domain.tts.service import TTSService
from app.domain.camera.service import CameraService
from app.infra.translator import TranslatorService


@dataclass
class Deps:
    config: Config
    detection: DetectionService
    ocr: OCRService
    scene: SceneService
    tts: TTSService
    camera: CameraService
    translator: TranslatorService
