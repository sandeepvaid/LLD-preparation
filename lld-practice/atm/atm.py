from states.idle_state import IdleState
from states.card_inserted_state import CardInsertedState
from states.transaction_state import TransactionState
from service.card_service import CardService


class ATM:
    def __init__(self):
        self.idle_state = IdleState(self)
        self.card_inserted_state = CardInsertedState(self)
        self.transaction_state = TransactionState(self)
        self.state = self.idle_state

        self.card_service = CardService()
        self.current_card = None
        self.pin_attempts = 0

    # --- CardService wrappers (states never touch card_service directly) ---
    def verify_card(self, card_number: str) -> bool:
        return self.card_service.verify_card(card_number)

    def verify_pin(self, pin: str) -> bool:
        return self.card_service.verify_pin(self.current_card, pin)

    def get_balance(self) -> float:
        return self.card_service.get_balance(self.current_card)

    def deduct(self, amount: float) -> bool:
        return self.card_service.deduct(self.current_card, amount)

    def reset_session(self):
        self.current_card = None
        self.pin_attempts = 0
        self.state = self.idle_state

    # --- Public actions (delegate to current state) ---
    def insert_card(self, card_number: str):
        self.state.insert_card(card_number)

    def enter_pin(self, pin: str):
        self.state.enter_pin(pin)

    def withdraw(self, amount: float, strategy):
        self.state.withdraw(amount, strategy)

    def view_balance(self):
        self.state.view_balance()

    def eject_card(self):
        self.state.eject_card()
