from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class EventType(Enum):
    CHEGADA = "CHEGADA"
    SAIDA = "SAIDA"
    PASSAGEM = "PASSAGEM"

@dataclass(order=True)
class Event:
    time: float = field(compare=True)
    type: EventType = field(compare=False)
    source: Optional[str] = field(default=None, compare=False)
    target: Optional[str] = field(default=None, compare=False)

    def __repr__(self):
        return (
            f"Event(time={self.time:.4f}, type={self.type.name}, "
            f"source={self.source}, target={self.target})"
        )
