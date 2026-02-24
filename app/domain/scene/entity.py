from dataclasses import dataclass


@dataclass
class SceneResult:
    caption: str
    detail: str
    caption_id: str = ""
    detail_id: str = ""
