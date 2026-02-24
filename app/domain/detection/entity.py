from dataclasses import dataclass


@dataclass
class DetectedObject:
    label: str
    name: str
    confidence: float


@dataclass
class DetectionResult:
    objects: list[DetectedObject]
    model_name: str = "MobileNetV2"
