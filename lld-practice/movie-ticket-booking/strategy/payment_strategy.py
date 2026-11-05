
from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> float:
        pass


class CashPaymentStrategy(PaymentStrategy):
    def pay(self, amount: float) -> float:
        print(f"Paid ${amount:.2f} in cash.")
        return amount