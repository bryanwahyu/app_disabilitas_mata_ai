from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.object_detection import ObjectDetectionService
from app.services.ocr_service import OCRService
from app.services.scene_service import SceneService
from app.utils.image_helper import load_image_from_upload

router = APIRouter(prefix="/api/v1/vision", tags=["DisabilitasKu Vision AI"])

object_detector = ObjectDetectionService()
ocr_service = OCRService()
scene_service = SceneService()


@router.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    """Deteksi objek dalam gambar untuk membantu tunanetra"""
    try:
        image = await load_image_from_upload(file)
        results = object_detector.detect(image)
        return {"success": True, "message": "Objek berhasil dideteksi", "data": {"objects": results}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ocr")
async def read_text(file: UploadFile = File(...)):
    """Baca teks dari gambar (OCR) untuk membantu tunanetra"""
    try:
        image = await load_image_from_upload(file)
        result = ocr_service.extract_text(image)
        return {"success": True, "message": "Teks berhasil dibaca", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/describe")
async def describe_scene(file: UploadFile = File(...)):
    """Deskripsikan scene/pemandangan dalam gambar untuk tunanetra"""
    try:
        image = await load_image_from_upload(file)
        result = scene_service.describe(image)
        return {"success": True, "message": "Scene berhasil dideskripsikan", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
