from dataclasses import asdict

from fastapi import APIRouter, UploadFile, File

from app.domain.detection.service import DetectionService
from app.pkg.image_helper import load_image_from_upload
from app.pkg.resp import success


def create_router(service: DetectionService) -> APIRouter:
    router = APIRouter(prefix="/api/v1/vision", tags=["Detection"])

    @router.post("/detect")
    async def detect_objects(file: UploadFile = File(...)):
        """Deteksi objek dalam gambar untuk membantu tunanetra"""
        image = await load_image_from_upload(file)
        result = service.detect(image)
        return success(
            "Objek berhasil dideteksi",
            {"objects": [asdict(obj) for obj in result.objects]},
        )

    return router
