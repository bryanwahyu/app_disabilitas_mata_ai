from dataclasses import asdict

from fastapi import APIRouter, UploadFile, File

from app.domain.ocr.service import OCRService
from app.pkg.image_helper import load_image_from_upload
from app.pkg.resp import success


def create_router(service: OCRService) -> APIRouter:
    router = APIRouter(prefix="/api/v1/vision", tags=["OCR"])

    @router.post("/ocr")
    async def read_text(file: UploadFile = File(...)):
        """Baca teks dari gambar (OCR) untuk membantu tunanetra"""
        image = await load_image_from_upload(file)
        result = service.extract_text(image)
        return success("Teks berhasil dibaca", asdict(result))

    return router
