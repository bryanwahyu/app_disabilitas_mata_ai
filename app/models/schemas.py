from pydantic import BaseModel
from typing import Optional


class DetectionResult(BaseModel):
    label: str
    confidence: float
    description: str


class OCRResult(BaseModel):
    text: str
    language: Optional[str] = None


class SceneDescription(BaseModel):
    description: str
    objects: list[str]
    suggestion: str


class AIResponse(BaseModel):
    success: bool
    message: str
    data: dict
