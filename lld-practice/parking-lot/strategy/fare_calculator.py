from strategy.fare_strategy import FareStrategy


class FareCalculator:
    def __init__(self, strategies: list):
        self.strategies = strategies   # [BaseFareStrategy, PeakHoursFareStrategy, ...]

    def calculate_fare(self, ticket) -> float:
        fare = 0.0
        for strategy in self.strategies:
            fare = strategy.calculate_fare(ticket, fare)
        return fare
