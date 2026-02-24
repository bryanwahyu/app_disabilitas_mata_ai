from fastapi import FastAPI
from app.routers import vision
from app.config import HOST, PORT

app = FastAPI(
    title="DisabilitasKu Vision AI",
    description="AI Visual Recognition untuk membantu penyandang tunanetra",
    version="1.0.0",
)

app.include_router(vision.router)


@app.get("/")
async def root():
    return {
        "app": "DisabilitasKu Vision AI",
        "version": "1.0.0",
        "endpoints": {
            "detect": "POST /api/v1/vision/detect - Deteksi objek",
            "ocr": "POST /api/v1/vision/ocr - Baca teks dari gambar",
            "describe": "POST /api/v1/vision/describe - Deskripsi scene",
        },
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
