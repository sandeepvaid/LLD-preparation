from states.state import State


class TransactionState(State):
    def insert_card(self, card_number):
        print("Session in progress. Please eject card first.")

    def enter_pin(self, pin):
        print("PIN already verified.")

    def withdraw(self, amount, strategy):
        # state only guards + delegates — no business logic here
        success = self.atm.deduct(amount)
        if success:
            strategy.dispense(amount, self.atm)

    def view_balance(self):
        balance = self.atm.get_balance()
        print(f"Current balance: ${balance:.2f}")

    def eject_card(self):
        print("Card ejected. Thank you.")
        self.atm.reset_session()
