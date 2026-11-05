from states.state import State

MAX_PIN_ATTEMPTS = 3


class CardInsertedState(State):
    def insert_card(self, card_number):
        print("Card already inserted.")

    def enter_pin(self, pin):
        if not self.atm.verify_pin(pin):
            self.atm.pin_attempts += 1
            remaining = MAX_PIN_ATTEMPTS - self.atm.pin_attempts
            if remaining == 0:
                print("Too many wrong attempts. Card blocked.")
                self.atm.reset_session()
                return
            print(f"Wrong PIN. {remaining} attempt(s) left.")
            return
        self.atm.pin_attempts = 0
        print("PIN verified. You can now transact.")
        self.atm.state = self.atm.transaction_state

    def withdraw(self, amount, strategy):
        print("Please verify your PIN first.")

    def view_balance(self):
        print("Please verify your PIN first.")

    def eject_card(self):
        print("Card ejected.")
        self.atm.reset_session()
