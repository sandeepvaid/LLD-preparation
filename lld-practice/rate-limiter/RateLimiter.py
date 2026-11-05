from manager.RateLimiterRegistry import RateLimiterRegistry


class RateLimiter:
    def __init__(self, registry: RateLimiterRegistry):
        self.registry = registry

    def allow_request(self, key: str) -> bool:
        return self.registry.get_or_create(key).allow_request()
