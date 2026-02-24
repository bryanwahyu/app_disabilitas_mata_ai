"""BLIP model wrapper — acts as repository in DDD terms."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.config.config import SceneModelConfig

if TYPE_CHECKING:
    from PIL import Image


class BLIPRepository:
    def __init__(self, config: SceneModelConfig):
        self.config = config
        self._processor = None
        self._model = None

    def _load_model(self):
        from transformers import BlipProcessor, BlipForConditionalGeneration

        self._processor = BlipProcessor.from_pretrained(self.config.model_name)
        self._model = BlipForConditionalGeneration.from_pretrained(self.config.model_name)

    def caption(self, image: Image.Image) -> str:
        if self._model is None:
            self._load_model()

        inputs = self._processor(image, return_tensors="pt")
        output = self._model.generate(**inputs, max_new_tokens=self.config.max_tokens)
        return self._processor.decode(output[0], skip_special_tokens=True)

    def caption_conditional(self, image: Image.Image, prompt: str = "a detailed photo of") -> str:
        if self._model is None:
            self._load_model()

        inputs = self._processor(image, prompt, return_tensors="pt")
        output = self._model.generate(**inputs, max_new_tokens=self.config.max_tokens)
        return self._processor.decode(output[0], skip_special_tokens=True)
