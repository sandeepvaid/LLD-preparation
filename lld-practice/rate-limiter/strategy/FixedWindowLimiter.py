from strategy.RateLimiterStrategy import RateLimiterStrategy
from time import monotonic


class FixedWindowLimiter(RateLimiterStrategy):

    def __init__(self, max_requests, window_size):
        self.max_requests = max_requests
        self.window_size = window_size
        self.request_count = 0
        self.window_start_time = monotonic()

    def allow_request(self) -> bool:
        current_time = monotonic()
        if current_time - self.window_start_time >= self.window_size:
            self.window_start_time = current_time
            self.request_count = 0

        if self.request_count < self.max_requests:
            self.request_count += 1
            return True
        return False
