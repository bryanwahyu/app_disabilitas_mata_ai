import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

CONFIG_DIR = Path(__file__).resolve().parent.parent.parent / "config"


@dataclass
class ServerConfig:
    host: str = "0.0.0.0"
    port: int = 8000


@dataclass
class DetectionModelConfig:
    name: str = "MobileNetV2"
    top_k: int = 5


@dataclass
class OCRModelConfig:
    languages: str = "ind+eng"


@dataclass
class SceneModelConfig:
    model_name: str = "Salesforce/blip-image-captioning-large"
    max_tokens: int = 100


@dataclass
class TranslatorModelConfig:
    model_name: str = "Helsinki-NLP/opus-mt-en-id"


@dataclass
class TTSModelConfig:
    language: str = "id"
    slow: bool = False


@dataclass
class CameraConfig:
    max_fps: int = 10
    frame_quality: int = 80


@dataclass
class ModelsConfig:
    detection: DetectionModelConfig = field(default_factory=DetectionModelConfig)
    ocr: OCRModelConfig = field(default_factory=OCRModelConfig)
    scene: SceneModelConfig = field(default_factory=SceneModelConfig)
    translator: TranslatorModelConfig = field(default_factory=TranslatorModelConfig)
    tts: TTSModelConfig = field(default_factory=TTSModelConfig)


@dataclass
class AppConfig:
    name: str = "DisabilitasKu Vision AI"
    version: str = "2.0.0"
    description: str = "AI Visual Recognition untuk membantu penyandang tunanetra"


@dataclass
class Config:
    app: AppConfig = field(default_factory=AppConfig)
    server: ServerConfig = field(default_factory=ServerConfig)
    models: ModelsConfig = field(default_factory=ModelsConfig)
    camera: CameraConfig = field(default_factory=CameraConfig)


def load_config() -> Config:
    """Load config from YAML file, with env var overrides."""
    yaml_path = CONFIG_DIR / "app.yaml"
    data = {}
    if yaml_path.exists():
        with open(yaml_path) as f:
            data = yaml.safe_load(f) or {}

    cfg = Config(
        app=AppConfig(**data.get("app", {})),
        server=ServerConfig(**data.get("server", {})),
        models=ModelsConfig(
            detection=DetectionModelConfig(**data.get("models", {}).get("detection", {})),
            ocr=OCRModelConfig(**data.get("models", {}).get("ocr", {})),
            scene=SceneModelConfig(**data.get("models", {}).get("scene", {})),
            translator=TranslatorModelConfig(**data.get("models", {}).get("translator", {})),
            tts=TTSModelConfig(**data.get("models", {}).get("tts", {})),
        ),
        camera=CameraConfig(**data.get("camera", {})),
    )

    # Env var overrides
    if host := os.getenv("HOST"):
        cfg.server.host = host
    if port := os.getenv("PORT"):
        cfg.server.port = int(port)

    return cfg
