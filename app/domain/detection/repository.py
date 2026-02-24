"""MobileNetV2 model wrapper — acts as repository in DDD terms."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.config.config import DetectionModelConfig
from app.domain.detection.entity import DetectedObject

if TYPE_CHECKING:
    from PIL import Image


class MobileNetRepository:
    def __init__(self, config: DetectionModelConfig):
        self.config = config
        self._model = None
        self._preprocess = None

    def _load_model(self):
        from tensorflow.keras.applications import MobileNetV2
        from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

        self._model = MobileNetV2(weights="imagenet")
        self._preprocess = preprocess_input

    def predict(self, image: Image.Image) -> list[DetectedObject]:
        import numpy as np
        from tensorflow.keras.applications.mobilenet_v2 import decode_predictions

        if self._model is None:
            self._load_model()

        img = image.resize((224, 224))
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = self._preprocess(img_array)

        predictions = self._model.predict(img_array)
        results = decode_predictions(predictions, top=self.config.top_k)[0]

        return [
            DetectedObject(label=label, name=name, confidence=float(conf))
            for label, name, conf in results
        ]
