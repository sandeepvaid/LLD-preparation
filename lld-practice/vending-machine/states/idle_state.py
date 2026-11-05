from states.state import State


class IdleState(State):
    def insert_coin(self, amount):
        if self.vm.payment_strategy is None:
            print("Please choose a payment method before inserting coins.")
            return
        self.vm.balance += amount
        print(f"Inserted ${amount:.2f}. Current balance: ${self.vm.balance:.2f}")
        self.vm.state = self.vm.has_money_state

    def select_item(self, code):
        print("Please insert a coin first")

    def refund(self):
        print("No coin to refund")
