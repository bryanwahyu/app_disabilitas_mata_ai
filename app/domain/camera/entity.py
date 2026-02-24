from dataclasses import dataclass, field


@dataclass
class FrameResult:
    objects: list[dict] = field(default_factory=list)
    frame_index: int = 0
