from dataclasses import dataclass
from typing import Optional


@dataclass
class RoutingProbability:
    target: Optional[str]
    probability: float
