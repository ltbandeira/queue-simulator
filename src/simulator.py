import heapq
from typing import List, Optional
from .event import Event, EventType
from .queue_top import Queue
from .random_generator import RandomGeneratorForQueue


class Simulator:
    def __init__(
        self,
        scheduler: List[Event],
        rnd: RandomGeneratorForQueue,
        queues: List[Queue]
    ):
        self.scheduler = scheduler
        heapq.heapify(self.scheduler)
        self.rnd = rnd
        self.queues = {q.id: q for q in queues}
        self.global_time = 0.0
        for q in self.queues.values():
            q.reset()

    def run(self):
        while self.rnd.has_numbers() and self.scheduler:
            event = heapq.heappop(self.scheduler)
            self._advance_time(event.time)
            if event.type == EventType.CHEGADA:
                self._handle_arrival(event)
            elif event.type == EventType.SAIDA:
                self._handle_departure(event)
            else:
                self._handle_passage(event)
        self.display_results()

    def _advance_time(self, new_time: float):
        delta = new_time - self.global_time
        self.global_time = new_time
        for q in self.queues.values():
            idx = q.status()
            if idx >= len(q.queue_times):
                q.queue_times.extend([0.0] * (idx + 1 - len(q.queue_times)))
            q.queue_times[idx] += delta

    def _random_between(self, low: float, high: float) -> float:
        return low + (high - low) * self.rnd.next_random()

    def _schedule_event(
        self,
        etype: EventType,
        delay: float,
        source: Optional[str],
        target: Optional[str]
    ):
        heapq.heappush(
            self.scheduler,
            Event(
                time=self.global_time + delay,
                type=etype,
                source=source,
                target=target
            )
        )

    def _handle_arrival(self, ev: Event):
        q = self.queues[ev.target]
        
        # Se a fila de destino não está cheia, agendar a chegada
        if q.status() < q.capacity:
            q.in_queue()
            if q.status() <= q.servers:
                tgt = q.get_next_target(self.rnd)
                svc_delay = self._random_between(q.min_service, q.max_service)
                etype = EventType.PASSAGEM if tgt else EventType.SAIDA
                self._schedule_event(etype, svc_delay, q.id, tgt)
        else:
            q.record_loss()

        if q.min_arrival is not None:
            arr_delay = self._random_between(q.min_arrival, q.max_arrival)
            self._schedule_event(EventType.CHEGADA, arr_delay, None, q.id)

    def _handle_departure(self, ev: Event):
        q = self.queues[ev.source]
        q.out_queue()
        
        # Se a fila de origem ainda tem clientes, agendar o próximo
        if q.status() >= q.servers:
            tgt = q.get_next_target(self.rnd)
            delay = self._random_between(q.min_service, q.max_service)
            etype = EventType.PASSAGEM if tgt else EventType.SAIDA
            self._schedule_event(etype, delay, q.id, tgt)

    def _handle_passage(self, ev: Event):
        src_q = self.queues[ev.source]
        tgt_q = self.queues[ev.target]
        
        # Partida da fila de origem
        src_q.out_queue()
        if src_q.status() >= src_q.servers:
            nxt = src_q.get_next_target(self.rnd)
            d = self._random_between(src_q.min_service, src_q.max_service)
            et = EventType.PASSAGEM if nxt else EventType.SAIDA
            self._schedule_event(et, d, src_q.id, nxt)
        
        # Chegada na fila de destino
        if tgt_q.status() < tgt_q.capacity:
            tgt_q.in_queue()
            if tgt_q.status() <= tgt_q.servers:
                nxt2 = tgt_q.get_next_target(self.rnd)
                d2 = self._random_between(tgt_q.min_service, tgt_q.max_service)
                et2 = EventType.PASSAGEM if nxt2 else EventType.SAIDA
                self._schedule_event(et2, d2, tgt_q.id, nxt2)
        else:
            tgt_q.record_loss()

    def display_results(self):
        total = self.global_time
        for q in self.queues.values():
            cap = '' if q.capacity == float('inf') else f"/{int(q.capacity)}"
            print(f"Fila: {q.id} (G/G/{q.servers}{cap})")
            print(f"Serviço: {q.min_service} ... {q.max_service}")
            print("State   Time      Probability")
            for i, t in enumerate(q.queue_times):
                if t <= 0:
                    continue
                pct = t / total * 100
                print(f"  {i:<5} {t:>8.4f} {pct:>7.2f}%")
            print(f"Clientes perdidos: {q.loss_count}\n")
        print(f"Tempo total de simulação: {total:.4f}")
