"""gTTS wrapper — acts as repository in DDD terms."""

import io

from app.config.config import TTSModelConfig
from app.domain.tts.entity import TTSResult


class GTTSRepository:
    def __init__(self, config: TTSModelConfig):
        self.config = config

    def synthesize(self, text: str) -> TTSResult:
        from gtts import gTTS

        tts = gTTS(text=text, lang=self.config.language, slow=self.config.slow)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)

        return TTSResult(audio_bytes=buf.read(), language=self.config.language)
