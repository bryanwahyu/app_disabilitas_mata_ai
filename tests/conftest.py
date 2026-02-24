"""Test configuration — mock services, TestClient, fixtures."""

from dataclasses import dataclass
from io import BytesIO
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.config.config import (
    Config, AppConfig, ServerConfig, ModelsConfig, CameraConfig,
    DetectionModelConfig, OCRModelConfig, SceneModelConfig,
    TranslatorModelConfig, TTSModelConfig,
)
from app.domain.detection.entity import DetectedObject, DetectionResult
from app.domain.ocr.entity import OCRResult
from app.domain.scene.entity import SceneResult
from app.domain.tts.entity import TTSResult
from app.domain.camera.entity import FrameResult
from app.deps import Deps
from app.factory import create_app


def _test_config() -> Config:
    return Config(
        app=AppConfig(name="Test", version="0.0.1", description="Test"),
        server=ServerConfig(host="127.0.0.1", port=8000),
        models=ModelsConfig(
            detection=DetectionModelConfig(),
            ocr=OCRModelConfig(),
            scene=SceneModelConfig(),
            translator=TranslatorModelConfig(),
            tts=TTSModelConfig(),
        ),
        camera=CameraConfig(),
    )


@pytest.fixture
def mock_detection_service():
    svc = MagicMock()
    svc.detect.return_value = DetectionResult(
        objects=[
            DetectedObject(label="n01234", name="cat", confidence=0.95),
            DetectedObject(label="n05678", name="dog", confidence=0.80),
        ]
    )
    return svc


@pytest.fixture
def mock_ocr_service():
    svc = MagicMock()
    svc.extract_text.return_value = OCRResult(text="Hello World", language="ind+eng")
    return svc


@pytest.fixture
def mock_scene_service():
    svc = MagicMock()
    svc.describe.return_value = SceneResult(
        caption="a cat sitting on a table",
        detail="a detailed photo of a cat sitting on a wooden table",
        caption_id="seekor kucing duduk di atas meja",
        detail_id="foto detail seekor kucing duduk di atas meja kayu",
    )
    return svc


@pytest.fixture
def mock_tts_service():
    svc = MagicMock()
    svc.speak.return_value = TTSResult(audio_bytes=b"fake-audio-data", language="id")
    return svc


@pytest.fixture
def mock_camera_service():
    svc = MagicMock()
    svc.process_frame.return_value = FrameResult(
        objects=[{"label": "n01234", "name": "cat", "confidence": 0.95}],
        frame_index=0,
    )
    return svc


@pytest.fixture
def mock_translator():
    svc = MagicMock()
    svc.translate.return_value = "teks terjemahan"
    return svc


@pytest.fixture
def app_with_mocks(
    mock_detection_service,
    mock_ocr_service,
    mock_scene_service,
    mock_tts_service,
    mock_camera_service,
    mock_translator,
):
    """Create FastAPI app with all mocked services."""
    from fastapi import FastAPI
    from app.http.router import register_routes
    from app.http.middleware.error_handler import register_error_handler
    from app.http.middleware.timing import register_timing_middleware

    config = _test_config()
    deps = Deps(
        config=config,
        detection=mock_detection_service,
        ocr=mock_ocr_service,
        scene=mock_scene_service,
        tts=mock_tts_service,
        camera=mock_camera_service,
        translator=mock_translator,
    )

    app = FastAPI()
    register_timing_middleware(app)
    register_error_handler(app)
    register_routes(app, deps)
    return app


@pytest.fixture
def client(app_with_mocks):
    return TestClient(app_with_mocks)


@pytest.fixture
def sample_image_bytes() -> bytes:
    """Generate a small test image as bytes."""
    img = Image.new("RGB", (100, 100), color="red")
    buf = BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf.read()
