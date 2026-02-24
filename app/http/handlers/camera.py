import base64
import io
import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from PIL import Image

from app.domain.camera.service import CameraService


def create_router(service: CameraService) -> APIRouter:
    router = APIRouter(prefix="/api/v1/vision", tags=["Camera"])

    @router.websocket("/camera/stream")
    async def camera_stream(websocket: WebSocket):
        """WebSocket untuk real-time camera frame processing.

        Client mengirim frame sebagai base64 JSON:
            {"frame": "<base64-encoded-image>", "index": 0}

        Server membalas:
            {"objects": [...], "frame_index": 0}
        """
        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_text()
                payload = json.loads(data)

                frame_b64 = payload.get("frame", "")
                frame_index = payload.get("index", 0)

                image_bytes = base64.b64decode(frame_b64)
                image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

                result = service.process_frame(image, frame_index)
                await websocket.send_json({
                    "objects": result.objects,
                    "frame_index": result.frame_index,
                })
        except WebSocketDisconnect:
            pass
        except Exception as e:
            await websocket.send_json({"error": str(e)})
            await websocket.close()

    return router
