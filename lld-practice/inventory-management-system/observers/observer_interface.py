from abc import ABC, abstractmethod
class InventoryObserver(ABC):
    @abstractmethod
    def update(self, event):
        pass