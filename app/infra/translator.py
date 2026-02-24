"""Helsinki-NLP/opus-mt-en-id translator — free, local EN→ID translation."""

from app.config.config import TranslatorModelConfig


class TranslatorService:
    def __init__(self, config: TranslatorModelConfig):
        self.config = config
        self._tokenizer = None
        self._model = None

    def _load_model(self):
        from transformers import MarianMTModel, MarianTokenizer

        self._tokenizer = MarianTokenizer.from_pretrained(self.config.model_name)
        self._model = MarianMTModel.from_pretrained(self.config.model_name)

    def translate(self, text: str) -> str:
        if not text.strip():
            return ""

        if self._model is None:
            self._load_model()

        inputs = self._tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        translated = self._model.generate(**inputs)
        return self._tokenizer.decode(translated[0], skip_special_tokens=True)
