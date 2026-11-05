from states.idle_state import IdleState
from states.has_money_state import HasMoneyState
from states.dispensing_state import DispensingState
from payment.payment_strategy import PaymentStrategy
from inventory.inventory_management import InventoryManagement
from inventory.item import Item


class VendingMachine:
    def __init__(self):
        self.idle_state = IdleState(self)
        self.has_money_state = HasMoneyState(self)
        self.dispensing_state = DispensingState(self)
        self.state = self.idle_state
        self.balance = 0.0
        self.payment_strategy = None
        self.inventory = InventoryManagement()
        self.inventory.add_item("A1", Item("Soda", 1.5), 5)
        self.inventory.add_item("B2", Item("Chips", 2.0), 3)

    def get_slot(self, code):
        return self.inventory.get_slot(code)

    def remove_item(self, code, quantity):
        self.inventory.remove_item(code, quantity)

    def insert_coin(self, amount):
        self.state.insert_coin(amount)

    def choose_payment_strategy_and_pay(self, strategy: PaymentStrategy, amount):
        self.payment_strategy = strategy
        self.payment_strategy.pay(amount, self)

    def select_item(self, code):
        self.state.select_item(code)

    def refund(self):
        self.state.refund()
