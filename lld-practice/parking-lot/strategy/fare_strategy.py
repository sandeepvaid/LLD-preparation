from abc import ABC, abstractmethod


class FareStrategy(ABC):

    @abstractmethod
    def calculate_fare(self, ticket, current_fare: float) -> float:
        # current_fare is passed through the chain so each strategy
        # can build on top of what previous strategies calculated
        pass
