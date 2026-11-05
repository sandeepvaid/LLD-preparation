from states.state import State


class HasMoneyState(State):
    def insert_coin(self, amount):
        self.vm.balance += amount
        print(f"Inserted ${amount:.2f}. Current balance: ${self.vm.balance:.2f}")

    def select_item(self, code):
        slot = self.vm.get_slot(code)
        if slot is None or not slot.isAvailable:
            print("Invalid item code or out of stock.")
            return
        if self.vm.balance < slot.item.price:
            print(f"Insufficient balance. Please insert ${slot.item.price - self.vm.balance:.2f} more.")
            return
        self.vm.state = self.vm.dispensing_state
        self.vm.state._dispense_item(code)

    def refund(self):
        self.vm.balance = 0
        print("Refunded all coins. Current balance: $0.00")
