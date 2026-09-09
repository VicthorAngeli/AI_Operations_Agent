from __future__ import annotations

from collections import defaultdict, deque
from threading import Lock
from time import monotonic


class RateLimiter:
    """Process-local fixed-window limiter keyed by client address."""

    def __init__(self, max_requests: int = 30, window_seconds: int = 60) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def allow(self, key: str) -> tuple[bool, int]:
        now = monotonic()
        with self._lock:
            timestamps = self._requests[key]
            cutoff = now - self.window_seconds
            while timestamps and timestamps[0] <= cutoff:
                timestamps.popleft()
            if len(timestamps) >= self.max_requests:
                retry_after = max(1, int(timestamps[0] + self.window_seconds - now))
                return False, retry_after
            timestamps.append(now)
            return True, 0

    def reset(self) -> None:
        with self._lock:
            self._requests.clear()