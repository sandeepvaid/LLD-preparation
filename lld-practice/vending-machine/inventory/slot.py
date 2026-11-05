from inventory.item import Item


class Slot:
    def __init__(self, code: str, item: Item, quantity: int):
        self.code = code
        self.item = item
        self.quantity = quantity
        self.isAvailable = quantity > 0
