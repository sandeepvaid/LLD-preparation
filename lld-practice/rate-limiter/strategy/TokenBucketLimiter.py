from strategy.RateLimiterStrategy import RateLimiterStrategy
from time import monotonic


class TokenBucketLimiter(RateLimiterStrategy):

    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate     # tokens per second
        self.tokens = capacity
        self.last_refill_timestamp = monotonic()

    def allow_request(self) -> bool:
        # no background refill thread — lazily refill on each check
        current_time = monotonic()
        elapsed_time = current_time - self.last_refill_timestamp
        self.tokens = min(self.capacity, self.tokens + elapsed_time * self.refill_rate)
        self.last_refill_timestamp = current_time

        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
