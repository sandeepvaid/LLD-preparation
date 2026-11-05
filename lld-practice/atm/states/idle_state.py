from states.state import State


class IdleState(State):
    def insert_card(self, card_number):
        if not self.atm.verify_card(card_number):
            print("Invalid card.")
            return
        self.atm.current_card = card_number
        print("Card accepted. Please enter your PIN.")
        self.atm.state = self.atm.card_inserted_state

    def enter_pin(self, pin):
        print("Please insert your card first.")

    def withdraw(self, amount, strategy):
        print("Please insert your card first.")

    def view_balance(self):
        print("Please insert your card first.")

    def eject_card(self):
        print("No card inserted.")
