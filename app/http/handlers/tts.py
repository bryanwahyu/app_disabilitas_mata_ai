from fastapi import APIRouter
from fastapi.responses import Response
from pydantic import BaseModel

from app.domain.tts.service import TTSService


class TTSRequest(BaseModel):
    text: str


def create_router(service: TTSService) -> APIRouter:
    router = APIRouter(prefix="/api/v1/vision", tags=["TTS"])

    @router.post("/tts")
    async def text_to_speech(req: TTSRequest):
        """Ubah teks menjadi suara (Text-to-Speech) dalam Bahasa Indonesia"""
        result = service.speak(req.text)
        return Response(
            content=result.audio_bytes,
            media_type=result.content_type,
            headers={"Content-Disposition": "inline; filename=speech.mp3"},
        )

    return router
