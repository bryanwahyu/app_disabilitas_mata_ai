from dataclasses import dataclass


@dataclass
class TTSResult:
    audio_bytes: bytes
    content_type: str = "audio/mpeg"
    language: str = "id"
