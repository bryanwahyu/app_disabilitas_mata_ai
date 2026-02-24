from __future__ import annotations

from typing import TYPE_CHECKING

from app.domain.detection.entity import DetectionResult
from app.domain.detection.repository import MobileNetRepository

if TYPE_CHECKING:
    from PIL import Image


class DetectionService:
    def __init__(self, repository: MobileNetRepository):
        self.repo = repository

    def detect(self, image: Image.Image) -> DetectionResult:
        objects = self.repo.predict(image)
        return DetectionResult(objects=objects)
