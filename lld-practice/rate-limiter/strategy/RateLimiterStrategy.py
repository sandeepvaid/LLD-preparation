from abc import ABC, abstractmethod


class RateLimiterStrategy(ABC):

    @abstractmethod
    def allow_request(self) -> bool:
        pass
