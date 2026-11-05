from abc import ABC, abstractmethod


class State(ABC):
    def __init__(self, atm):
        self.atm = atm

    @abstractmethod
    def insert_card(self, card_number):
        pass

    @abstractmethod
    def enter_pin(self, pin):
        pass

    @abstractmethod
    def withdraw(self, amount, strategy):
        pass

    @abstractmethod
    def view_balance(self):
        pass

    @abstractmethod
    def eject_card(self):
        pass