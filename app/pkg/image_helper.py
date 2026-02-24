import io

from fastapi import UploadFile
from PIL import Image

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/bmp"}
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB


async def load_image_from_upload(file: UploadFile) -> Image.Image:
    """Load and validate image from upload file."""
    if file.content_type and file.content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError(f"Tipe file tidak didukung: {file.content_type}")

    contents = await file.read()

    if len(contents) > MAX_IMAGE_SIZE:
        raise ValueError("Ukuran file terlalu besar (maks 10MB)")

    image = Image.open(io.BytesIO(contents)).convert("RGB")
    return image
