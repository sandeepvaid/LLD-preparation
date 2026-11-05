import threading

from manager.inventory_manager import InventoryManager
from manager.product_catalog import ProductCatalog
from inventory_system import InventorySystem
from observers.low_stock_observer import LowStockNotifier


def basic_flow_demo():
    print("--- basic flow ---")
    manager = InventoryManager()
    catalog = ProductCatalog()
    system = InventorySystem(manager, catalog)

    print(system.create_product("prod_A", "Milk", 3.99))
    print(system.onboard_product("store_1", "prod_A", 10))
    print(system.deduct_stock("store_1", "prod_A", 4))                 # should succeed, 6 left
    print(system.deduct_stock("store_1", "prod_A", 100))                # should fail, insufficient stock
    print(system.onboard_product("store_1", "prod_A", 10))              # should fail, already onboarded
    print(system.deduct_stock("store_1", "prod_B", 1))                  # should fail, never onboarded
    print(system.add_stock("store_1", "prod_A", 20))                    # restock, 26 left
    print(system.deduct_stock("store_1", "prod_A", 26))                 # should now succeed
    print(system.remove_product_from_store("store_1", "prod_A"))       # soft-delete
    print(system.deduct_stock("store_1", "prod_A", 1))                  # should fail, deactivated
    print(system.remove_product_from_store("store_1", "prod_B"))       # should fail, never onboarded
    print()


def concurrency_demo():
    print("--- concurrency: 5 threads each deducting 3 units from a stock of 10 ---")
    manager = InventoryManager()
    catalog = ProductCatalog()
    system = InventorySystem(manager, catalog)
    system.create_product("prod_A", "Milk", 3.99)
    system.onboard_product("store_1", "prod_A", 10)

    results = []
    results_lock = threading.Lock()

    def worker(request_id):
        outcome = system.deduct_stock("store_1", "prod_A", 3)
        with results_lock:
            results.append((request_id, outcome))

    threads = [threading.Thread(target=worker, args=(f"request_{i}",)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    for request_id, outcome in results:
        print(f"{request_id}: {'succeeded' if outcome is True else 'failed'}")

    successes = sum(1 for _, outcome in results if outcome is True)
    record = manager.get_inventory(("store_1", "prod_A"))
    print(f"\nsuccessful deductions: {successes} (expected 3)")
    print(f"remaining quantity: {record.quantity} (expected 1)")
    assert successes == 3, "overselling occurred — lock failed to prevent it"
    assert record.quantity == 1, "quantity accounting is inconsistent with successful deduction count"
    print("no overselling — lock held correctly under concurrent access")


def low_stock_alert_demo():
    print("--- low-stock alerts: threshold=5, quantity=8 ---")
    manager = InventoryManager()
    catalog = ProductCatalog()
    system = InventorySystem(manager, catalog)
    system.subscribe_to_low_stock_alerts(LowStockNotifier())

    system.create_product("prod_A", "Milk", 3.99)
    manager.add_inventory("store_1", "prod_A", 8, low_stock_threshold=5)

    print("deduct(2) -> quantity=6, still above threshold, no alert expected:")
    system.deduct_stock("store_1", "prod_A", 2)
    print("deduct(3) -> quantity=3, crosses threshold, ONE alert expected:")
    system.deduct_stock("store_1", "prod_A", 3)
    print("deduct(1) -> quantity=2, already below threshold, NO repeat alert expected:")
    system.deduct_stock("store_1", "prod_A", 1)
    print()


def transfer_stock_demo():
    print("--- stock transfer between two stores ---")
    manager = InventoryManager()
    catalog = ProductCatalog()
    system = InventorySystem(manager, catalog)

    system.create_product("prod_A", "Milk", 3.99)
    system.onboard_product("store_1", "prod_A", 10)
    system.onboard_product("store_2", "prod_A", 2)

    print(system.transfer_stock("store_1", "store_2", "prod_A", 4))   # should succeed
    print(f"store_1 quantity: {manager.get_inventory(('store_1', 'prod_A')).quantity} (expected 6)")
    print(f"store_2 quantity: {manager.get_inventory(('store_2', 'prod_A')).quantity} (expected 6)")

    print(system.transfer_stock("store_1", "store_2", "prod_A", 100))  # should fail, insufficient
    print(system.transfer_stock("store_1", "store_3", "prod_A", 1))    # should fail, store_3 never onboarded
    print()


if __name__ == "__main__":
    basic_flow_demo()
    concurrency_demo()
    low_stock_alert_demo()
    transfer_stock_demo()
