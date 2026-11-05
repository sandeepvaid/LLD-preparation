from abc import ABC, abstractmethod


class State(ABC):
    def __init__(self, vending_machine):
        self.vm = vending_machine

    @abstractmethod
    def insert_coin(self, amount):
        pass

    @abstractmethod
    def select_item(self, code):
        pass

    @abstractmethod
    def refund(self):
        pass
