"""Orchestrates detection per frame for real-time camera processing."""

from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING

from app.config.config import CameraConfig
from app.domain.camera.entity import FrameResult
from app.domain.detection.service import DetectionService

if TYPE_CHECKING:
    from PIL import Image


class CameraService:
    def __init__(self, detection_service: DetectionService, config: CameraConfig):
        self.detection = detection_service
        self.config = config

    def process_frame(self, image: Image.Image, frame_index: int = 0) -> FrameResult:
        result = self.detection.detect(image)
        return FrameResult(
            objects=[asdict(obj) for obj in result.objects],
            frame_index=frame_index,
        )
