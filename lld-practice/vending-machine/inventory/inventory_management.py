from inventory.item import Item
from inventory.slot import Slot


class InventoryManagement:
    def __init__(self):
        self.slots = {}

    def add_item(self, code: str, item: Item, quantity: int):
        if code in self.slots:
            self.slots[code].quantity += quantity
        else:
            self.slots[code] = Slot(code, item, quantity)
        self.slots[code].isAvailable = True

    def get_slot(self, code: str):
        return self.slots.get(code)

    def remove_item(self, code: str, quantity: int):
        if code not in self.slots or self.slots[code].quantity < quantity:
            print("Not enough items in stock")
            return
        self.slots[code].quantity -= quantity
        if self.slots[code].quantity == 0:
            self.slots[code].isAvailable = False