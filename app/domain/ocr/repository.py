"""Tesseract OCR wrapper — acts as repository in DDD terms."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.config.config import OCRModelConfig
from app.domain.ocr.entity import OCRResult

if TYPE_CHECKING:
    from PIL import Image


class TesseractRepository:
    def __init__(self, config: OCRModelConfig):
        self.config = config

    def extract(self, image: Image.Image) -> OCRResult:
        import pytesseract

        text = pytesseract.image_to_string(image, lang=self.config.languages)
        return OCRResult(text=text.strip(), language=self.config.languages)
