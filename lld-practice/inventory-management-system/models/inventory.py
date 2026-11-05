import threading
class Inventory:
    def __init__(self,product_id,store_id,quantity,low_stock_threshold=5,observers=None):
        self.product_id = product_id
        self.store_id = store_id
        self.quantity = quantity
        self.low_stock_threshold = low_stock_threshold
        self.is_active = True
        self.observers = observers or []
        #here we use RLock instead of Lock because we might want to acquire the lock multiple times in the same thread (for example, if a method that acquires the lock calls another method that also acquires the lock). RLock allows the same thread to acquire the lock multiple times without causing a deadlock. In case of transfer stocks from two inventory objects, we will acquire the locks for both source and destination inventory objects in a consistent order to avoid deadlocks. This is done in the transfer_stock method of InventoryManager class.
        self._lock = threading.RLock()

    def deduct(self,qty):
        with self._lock:
            if not self.is_active:
                raise ValueError(f"product {self.product_id} at store {self.store_id} is discontinued")
            if self.quantity >= qty:
                #reason behind this is that we want to notify observers only when the stock goes from above the threshold to below or equal to the threshold. If the stock was already below or equal to the threshold, we don't need to notify again. This prevents multiple notifications for the same low stock condition.
                above_threshold = self.quantity > self.low_stock_threshold

                self.quantity -= qty

                if above_threshold and self.quantity <= self.low_stock_threshold:
                    self.notify_observers()

                return True
            else:
                return False
    def add(self,qty):
        with self._lock:
            self.quantity += qty
            return True

    def notify_observers(self):
        for observer in self.observers:
            observer.update((self.store_id, self.product_id, self.quantity, self.low_stock_threshold))

    def deactivate(self):
        with self._lock:
            self.is_active = False