from states.state import State


class DispensingState(State):
    def insert_coin(self, amount):
        print("Currently dispensing an item. Please wait.")

    def select_item(self, code):
        slot = self.vm.get_slot(code)
        print(f"Dispensing item {code}. Enjoy your {slot.item.name}!")

    def _dispense_item(self, code):
        slot = self.vm.get_slot(code)
        change = self.vm.balance - slot.item.price
        self.vm.remove_item(code, 1)
        self.vm.balance -= slot.item.price
        print(f"Dispensing {slot.item.name}. Change returned: ${change:.2f}")
        self.vm.state = self.vm.idle_state
        self.vm.payment_strategy = None

    def refund(self):
        print("Can't refund — item is dispensing.")
