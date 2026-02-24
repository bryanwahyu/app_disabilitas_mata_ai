# DisabilitasKu Vision AI

AI Visual Recognition untuk membantu penyandang tunanetra — mendeteksi objek, membaca teks, mendeskripsikan scene, dan mengubah hasil menjadi suara (TTS) dalam Bahasa Indonesia.

## Masalah yang Diselesaikan

Penyandang tunanetra membutuhkan bantuan untuk memahami lingkungan visual mereka. Layanan ini menyediakan:
- **Deteksi Objek** — identifikasi benda di sekitar pengguna
- **Pembacaan Teks (OCR)** — membaca teks dari gambar/foto dokumen
- **Deskripsi Scene** — menjelaskan pemandangan secara detail
- **Text-to-Speech** — mengubah hasil analisis menjadi suara Bahasa Indonesia
- **Kamera Real-time** — pemrosesan frame kamera secara langsung via WebSocket

## Arsitektur

```
┌─────────────────────────────────────────────────┐
│                   FastAPI App                    │
├──────────┬──────────┬──────────┬────────────────┤
│ /detect  │  /ocr    │/describe │  /tts  /camera │
├──────────┴──────────┴──────────┴────────────────┤
│              Domain Services (DDD)               │
├──────────┬──────────┬──────────┬────────┬───────┤
│Detection │   OCR    │  Scene   │  TTS   │Camera │
├──────────┼──────────┼──────────┼────────┼───────┤
│MobileNet │Tesseract │  BLIP    │  gTTS  │  WS   │
│  V2      │  OCR     │(HF)     │        │       │
└──────────┴──────────┴────┬─────┴────────┴───────┘
                           │
                    Helsinki-NLP
                    (EN → ID Translator)
```

Menggunakan pola **Domain-Driven Design (DDD)**:
- `entity.py` — data model
- `repository.py` — wrapper AI model (memungkinkan mocking saat testing)
- `service.py` — business logic

## Tech Stack

| Komponen | Teknologi | Keterangan |
|---|---|---|
| Web Framework | FastAPI | Async, auto-docs |
| Object Detection | MobileNetV2 (TensorFlow) | ImageNet pre-trained |
| OCR | Tesseract | Indonesia + English |
| Scene Description | BLIP (Hugging Face) | Image captioning |
| Translation | Helsinki-NLP/opus-mt-en-id | EN→ID, lokal |
| Text-to-Speech | gTTS | Bahasa Indonesia |
| Real-time | WebSocket | Bidirectional camera stream |

Semua model **gratis dan open-source** — tidak memerlukan API key.

## API Endpoints

| Endpoint | Method | Deskripsi |
|---|---|---|
| `/health` | GET | Health check |
| `/api/v1/vision/detect` | POST | Deteksi objek (upload gambar) |
| `/api/v1/vision/ocr` | POST | Baca teks dari gambar |
| `/api/v1/vision/describe` | POST | Deskripsi scene + terjemahan ID |
| `/api/v1/vision/tts` | POST | Text-to-Speech (JSON body) |
| `/api/v1/vision/camera/stream` | WS | Real-time camera stream |

### Contoh Request

```bash
# Deteksi objek
curl -X POST http://localhost:8000/api/v1/vision/detect \
  -F "file=@photo.jpg"

# OCR
curl -X POST http://localhost:8000/api/v1/vision/ocr \
  -F "file=@document.png"

# Deskripsi scene
curl -X POST http://localhost:8000/api/v1/vision/describe \
  -F "file=@scene.jpg"

# Text-to-Speech
curl -X POST http://localhost:8000/api/v1/vision/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "Halo, selamat datang"}' \
  --output speech.mp3
```

### Response Format

Semua endpoint menggunakan envelope standar:

```json
{
  "success": true,
  "message": "Objek berhasil dideteksi",
  "data": { ... }
}
```

## Quick Start

### Lokal

```bash
# Install dependencies
pip install -r requirements.txt

# Install Tesseract (macOS)
brew install tesseract tesseract-lang

# Jalankan
make run
# atau
python main.py
```

### Docker

```bash
# Build dan jalankan
make docker-up

# Atau manual
docker compose up --build -d

# Verifikasi
curl http://localhost:8000/health
```

## Development

```bash
# Install dependencies
make install

# Jalankan dengan hot-reload
make run

# Jalankan tests
make test

# Lint
make lint

# Fix lint
make lint-fix
```

## Struktur Folder

```
app_disabilitas_mata_ai/
├── main.py                    # Entry point
├── config/app.yaml            # YAML config
├── app/
│   ├── config/config.py       # Config loader
│   ├── deps.py                # Dependency container
│   ├── factory.py             # App factory
│   ├── domain/                # Bounded contexts (DDD)
│   │   ├── detection/         # Object Detection
│   │   ├── ocr/               # OCR Text Reader
│   │   ├── scene/             # Scene Description
│   │   ├── tts/               # Text-to-Speech
│   │   └── camera/            # Real-time Camera
│   ├── http/                  # HTTP layer
│   │   ├── router.py          # Central routes
│   │   ├── handlers/          # Endpoint handlers
│   │   └── middleware/        # Error handler, timing
│   ├── infra/                 # Infrastructure
│   │   └── translator.py      # EN→ID translation
│   └── pkg/                   # Shared utilities
│       ├── resp.py            # Response envelope
│       └── image_helper.py    # Image load/validate
├── tests/                     # pytest test suite
├── Dockerfile                 # Multi-stage build
├── docker-compose.yml
└── Makefile
```
