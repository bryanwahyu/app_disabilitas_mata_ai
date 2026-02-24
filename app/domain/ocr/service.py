from __future__ import annotations

from typing import TYPE_CHECKING

from app.domain.ocr.entity import OCRResult
from app.domain.ocr.repository import TesseractRepository

if TYPE_CHECKING:
    from PIL import Image


class OCRService:
    def __init__(self, repository: TesseractRepository):
        self.repo = repository

    def extract_text(self, image: Image.Image) -> OCRResult:
        return self.repo.extract(image)
