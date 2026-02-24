from dataclasses import asdict

from fastapi import APIRouter, UploadFile, File

from app.domain.scene.service import SceneService
from app.pkg.image_helper import load_image_from_upload
from app.pkg.resp import success


def create_router(service: SceneService) -> APIRouter:
    router = APIRouter(prefix="/api/v1/vision", tags=["Scene"])

    @router.post("/describe")
    async def describe_scene(file: UploadFile = File(...)):
        """Deskripsikan scene/pemandangan dalam gambar untuk tunanetra"""
        image = await load_image_from_upload(file)
        result = service.describe(image)
        return success("Scene berhasil dideskripsikan", asdict(result))

    return router
