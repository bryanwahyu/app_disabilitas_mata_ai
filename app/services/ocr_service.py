# DisabilitasKu Vision AI - OCR Service
# Menggunakan Tesseract OCR untuk membaca teks dari gambar

from PIL import Image


class OCRService:
    def extract_text(self, image: Image.Image) -> dict:
        """Ekstrak teks dari gambar menggunakan Tesseract"""
        import pytesseract

        text = pytesseract.image_to_string(image, lang="ind+eng")
        return {
            "text": text.strip(),
            "language": "id/en",
        }
