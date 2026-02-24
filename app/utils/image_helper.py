import io
from PIL import Image
from fastapi import UploadFile


async def load_image_from_upload(file: UploadFile) -> Image.Image:
    """Load dan validasi image dari upload file"""
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    return image
