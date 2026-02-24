from app.domain.tts.entity import TTSResult
from app.domain.tts.repository import GTTSRepository


class TTSService:
    def __init__(self, repository: GTTSRepository):
        self.repo = repository

    def speak(self, text: str) -> TTSResult:
        if not text.strip():
            raise ValueError("Teks tidak boleh kosong")
        return self.repo.synthesize(text)
