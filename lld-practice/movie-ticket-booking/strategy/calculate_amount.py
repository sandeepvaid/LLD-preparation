
from abc import ABC, abstractmethod


class CalculateAmountStrategy(ABC):
    @abstractmethod
    def calculate_amount(self, seats, seat_price):
        pass


class RegularCalculateAmountStrategy(CalculateAmountStrategy):
    def calculate_amount(self, seats, seat_price):
        return len(seats) * seat_price