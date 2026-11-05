# PATTERN: Manager (Repository / Inventory)
# PURPOSE: Owns and manages a collection of domain objects (items, slots, rooms, floors).
#          Exposes clean CRUD methods so the context and states never touch
#          the raw collection directly. This is not a GoF pattern — it is a
#          structural layer you add whenever the system manages a collection.
#
# HOW TO USE:
#   1. Identify what your system manages (inventory slots, parking spots, rooms, accounts)
#   2. Create a Manager class that wraps a dict/list of those objects
#   3. Expose: get(), add(), remove(), is_available()
#   4. The context exposes thin wrappers (context.get_slot, context.remove_item)
#      so states only talk to the context, never to the manager directly.
#      (Law of Demeter: state → context → manager, not state → context.manager → ...)


class BaseManager:
    def __init__(self):
        self._store = {}   # key → domain object (Slot, Room, ParkingSpot, etc.)

    def add(self, key, item):
        self._store[key] = item

    def get(self, key):
        return self._store.get(key)

    def remove(self, key):
        return self._store.pop(key, None)

    def is_available(self, key):
        item = self.get(key)
        return item is not None
