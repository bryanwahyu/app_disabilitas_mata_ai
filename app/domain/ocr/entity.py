from dataclasses import dataclass


@dataclass
class OCRResult:
    text: str
    language: str
