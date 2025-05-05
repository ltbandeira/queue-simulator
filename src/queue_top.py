from typing import Optional, List
from .router import RoutingProbability
from .random_generator import RandomGeneratorForQueue


class Queue:
    def __init__(
        self,
        queue_id: str,
        servers: int,
        capacity: Optional[int],
        min_arrival: Optional[float],
        max_arrival: Optional[float],
        min_service: float,
        max_service: float,
        routing: List[RoutingProbability]
    ):
        self.id = queue_id
        self.servers = servers
        self.capacity = capacity if capacity >= 0 else float('inf')
        self.min_arrival = min_arrival
        self.max_arrival = max_arrival
        self.min_service = min_service
        self.max_service = max_service
        self.routing = routing
        self._size = 0
        self.loss_count = 0
        self.queue_times: List[float] = []

    def in_queue(self):
        self._size += 1

    def out_queue(self):
        self._size -= 1

    def status(self) -> int:
        return self._size

    def record_loss(self):
        self.loss_count += 1

    def reset(self):
        self._size = 0
        self.loss_count = 0
        self.queue_times.clear()

    def get_next_target(self, rnd: RandomGeneratorForQueue) -> Optional[str]:
        if len(self.routing) <= 1:
            return self.routing[0].target
        r = rnd.next_random()
        cum = 0.0
        for rp in self.routing:
            cum += rp.probability
            if r < cum:
                return rp.target
        return None
