from abc import ABC, abstractmethod


class PaymentStrategy(ABC):

    @abstractmethod
    def pay(self, amount, vending_machine):
        pass

    @abstractmethod
    def refund(self, amount, vending_machine):
        pass

    @abstractmethod
    def cancel(self):
        pass
