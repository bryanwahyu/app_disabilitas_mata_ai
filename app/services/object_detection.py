# DisabilitasKu Vision AI - Object Detection Service
# Menggunakan TensorFlow/Keras pre-trained model (MobileNetV2)

from PIL import Image
import numpy as np


class ObjectDetectionService:
    def __init__(self):
        self.model = None

    def load_model(self):
        """Load MobileNetV2 pre-trained model"""
        from tensorflow.keras.applications import MobileNetV2
        from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
        self.model = MobileNetV2(weights="imagenet")
        self.preprocess = preprocess_input

    def detect(self, image: Image.Image) -> list[dict]:
        """Deteksi objek dalam gambar"""
        from tensorflow.keras.applications.mobilenet_v2 import decode_predictions

        if self.model is None:
            self.load_model()

        img = image.resize((224, 224))
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = self.preprocess(img_array)

        predictions = self.model.predict(img_array)
        results = decode_predictions(predictions, top=5)[0]

        return [
            {"label": label, "confidence": float(conf), "description": name}
            for (label, name, conf) in results
        ]
