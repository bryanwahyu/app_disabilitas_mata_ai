# DisabilitasKu Vision AI - Scene Description Service
# Menggunakan BLIP (Salesforce) dari Hugging Face - gratis & lokal

from PIL import Image


class SceneService:
    def __init__(self):
        self.processor = None
        self.model = None

    def _load_model(self):
        """Load BLIP model dari Hugging Face (gratis, jalan lokal)"""
        from transformers import BlipProcessor, BlipForConditionalGeneration

        self.processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-large"
        )
        self.model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-large"
        )

    def describe(self, image: Image.Image) -> dict:
        """Deskripsikan scene dalam gambar untuk tunanetra"""
        if self.model is None:
            self._load_model()

        # Unconditional captioning
        inputs = self.processor(image, return_tensors="pt")
        output = self.model.generate(**inputs, max_new_tokens=100)
        caption = self.processor.decode(output[0], skip_special_tokens=True)

        # Conditional captioning - detail lebih
        detail_prompt = "a detailed photo of"
        inputs_detail = self.processor(image, detail_prompt, return_tensors="pt")
        output_detail = self.model.generate(**inputs_detail, max_new_tokens=100)
        detail = self.processor.decode(output_detail[0], skip_special_tokens=True)

        return {
            "description": caption,
            "detail": detail,
            "objects": [],
            "suggestion": "",
        }
