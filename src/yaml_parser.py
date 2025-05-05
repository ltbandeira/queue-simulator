import yaml
import heapq
from typing import Dict, Any, List, Tuple

from .event import Event, EventType
from .random_generator import RandomGeneratorForQueue
from .queue_top import Queue
from .router import RoutingProbability


class YamlParser:
    def __init__(self, path: str):
        self.path = path

    def load(self) -> Tuple[List[Event], RandomGeneratorForQueue, List[Queue]]:
        data = self._read_yaml()
        scheduler = self._build_scheduler(data)
        rnd = self._build_random_generator(data)
        routing = self._build_routing(data)
        queues = self._build_queues(data, routing)
        return scheduler, rnd, queues

    def _read_yaml(self) -> Dict[str, Any]:
        with open(self.path, 'r') as f:
            return yaml.safe_load(f) or {}

    def _build_scheduler(self, data: Dict[str, Any]) -> List[Event]:
        scheduler: List[Event] = []
        for queue_id, arrival_time in data.get('arrivals', {}).items():
            event = Event(
                time=float(arrival_time),
                type=EventType.CHEGADA,
                source=None,
                target=queue_id
            )
            heapq.heappush(scheduler, event)
        return scheduler

    def _build_random_generator(self, data: Dict[str, Any]) -> RandomGeneratorForQueue:
        seed = data.get('seed')
        max_n = data.get('rndnumbersPerSeed')
        arr = data.get('rndnumbers')
        if seed is not None:
            return RandomGeneratorForQueue(seed=int(seed), max_numbers=int(max_n))
        else:
            return RandomGeneratorForQueue(arr_mock=list(arr or []))

    def _build_routing(self, data: Dict[str, Any]) -> Dict[str, List[RoutingProbability]]:
        routing_map: Dict[str, List[RoutingProbability]] = {}
        for edge in data.get('network', []):
            src = edge['source']
            tgt = edge.get('target')
            prob = edge['probability']
            routing_map.setdefault(src, []).append(
                RoutingProbability(target=tgt, probability=float(prob))
            )
        for src, probs in routing_map.items():
            total = sum(rp.probability for rp in probs)
            if total < 1.0:
                probs.append(RoutingProbability(
                    target=None, probability=1.0 - total))
        return routing_map

    def _build_queues(
        self,
        data: Dict[str, Any],
        routing: Dict[str, List[RoutingProbability]]
    ) -> List[Queue]:
        queues: List[Queue] = []
        for queue_id, cfg in data.get('queues', {}).items():
            params = cfg.copy()
            servers = int(params['servers'])
            capacity = int(params.get('capacity', -1))
            min_arr = params.get('minArrival')
            max_arr = params.get('maxArrival')
            min_srv = float(params['minService'])
            max_srv = float(params['maxService'])
            routing_probs = routing.get(
                queue_id, [RoutingProbability(target=None, probability=1.0)])
            queues.append(
                Queue(
                    queue_id=queue_id,
                    servers=servers,
                    capacity=capacity,
                    min_arrival=float(
                        min_arr) if min_arr is not None else None,
                    max_arrival=float(
                        max_arr) if max_arr is not None else None,
                    min_service=min_srv,
                    max_service=max_srv,
                    routing=routing_probs
                )
            )
        return queues
