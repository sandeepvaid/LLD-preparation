from observers.observer_interface import InventoryObserver

class LowStockNotifier(InventoryObserver):
    def update(self, event):
        store_id, product_id, quantity, threshold = event
        print(f"[ALERT] Low stock at store {store_id} for product {product_id}: only {quantity} left (threshold: {threshold})")