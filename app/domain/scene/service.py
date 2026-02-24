from __future__ import annotations

from typing import TYPE_CHECKING

from app.domain.scene.entity import SceneResult
from app.domain.scene.repository import BLIPRepository
from app.infra.translator import TranslatorService

if TYPE_CHECKING:
    from PIL import Image


class SceneService:
    def __init__(self, repository: BLIPRepository, translator: TranslatorService):
        self.repo = repository
        self.translator = translator

    def describe(self, image: Image.Image) -> SceneResult:
        caption = self.repo.caption(image)
        detail = self.repo.caption_conditional(image)

        caption_id = self.translator.translate(caption)
        detail_id = self.translator.translate(detail)

        return SceneResult(
            caption=caption,
            detail=detail,
            caption_id=caption_id,
            detail_id=detail_id,
        )
