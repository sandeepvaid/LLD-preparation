from abc import ABC, abstractmethod


class WithdrawStrategy(ABC):

    @abstractmethod
    def dispense(self, amount, atm):
        pass
