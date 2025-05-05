class RandomGeneratorForQueue:
    _a = 1664525
    _c = 1013904223
    _M = 2**32

    def __init__(
        self,
        seed: int = None,
        max_numbers: int = None,
        arr_mock: list = None
    ):
        if arr_mock is not None:
            self._arr = arr_mock
            self._max = len(arr_mock)
            self._count = 0
            self._prev = None
        else:
            self._arr = None
            self._max = max_numbers
            self._count = 0
            self._prev = seed or 0

    def next_random(self) -> float:
        if not self.has_numbers():
            return -1.0
        if self._arr is not None:
            val = self._arr[self._count]
            self._count += 1
            return val
        self._prev = (self._a * self._prev + self._c) % self._M
        self._count += 1
        return self._prev / self._M

    def has_numbers(self) -> bool:
        return self._count < self._max