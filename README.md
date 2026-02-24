# DisabilitasKu Vision AI

AI Visual Recognition untuk membantu penyandang tunanetra.

## Tech Stack
- Python + FastAPI
- TensorFlow/Keras (MobileNetV2 - Object Detection)
- Hugging Face BLIP (Scene Description)
- Tesseract OCR (Text Reader)

## API Endpoints

| Endpoint | Method | Fungsi |
|---|---|---|
| `/api/v1/vision/detect` | POST | Deteksi objek dalam gambar |
| `/api/v1/vision/ocr` | POST | Baca teks dari gambar |
| `/api/v1/vision/describe` | POST | Deskripsi scene/pemandangan |
| `/health` | GET | Health check |

## Setup
```bash
pip install -r requirements.txt
python main.py
```
