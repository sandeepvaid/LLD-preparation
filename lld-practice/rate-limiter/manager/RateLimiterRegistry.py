class RateLimiterRegistry:
    def __init__(self, strategy_factory):
        self.rate_limiters = {}
        self.strategy_factory = strategy_factory   # zero-arg callable -> RateLimiterStrategy

    def get_or_create(self, key: str):
        if key not in self.rate_limiters:
            self.rate_limiters[key] = self.strategy_factory()
        return self.rate_limiters[key]
