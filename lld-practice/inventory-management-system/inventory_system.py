class InventorySystem:
    def __init__(self, inventory_manager, product_catalog):
        self.inventory_manager = inventory_manager
        self.product_catalog = product_catalog

    def create_product(self, product_id, name, price):
        try:
            self.product_catalog.create_product(product_id, name, price)
            return f"Product {product_id} ({name}) added to catalog."
        except ValueError as e:
            return f"Product creation failed: {e}"

    def onboard_product(self, store_id, product_id, quantity):
        product = self.product_catalog.get_product(product_id)
        if product is None:
            return f"Cannot onboard: product {product_id} not found in catalog."
        try:
            self.inventory_manager.add_inventory(store_id, product_id, quantity)
            return f"Product {product.name} ({product_id}) onboarded at store {store_id} with quantity {quantity}."
        except ValueError as e:
            return f"Onboarding failed: {e}"

    def add_stock(self, store_id, product_id, quantity):
        key = (store_id, product_id)
        try:
            self.inventory_manager.add_stock(key, quantity)
            return f"Stock updated for product {product_id} at store {store_id}."
        except ValueError as e:
            return f"Stock update failed: {e}"

    def deduct_stock(self, store_id, product_id, quantity):
        key = (store_id, product_id)
        try:
            if self.inventory_manager.deduct_stock(key, quantity):
                return True
            return False
        except ValueError as e:
            return f"Deduction failed: {e}"

    def transfer_stock(self, source_store_id, dest_store_id, product_id, quantity):
        source_key = (source_store_id, product_id)
        dest_key = (dest_store_id, product_id)
        try:
            if self.inventory_manager.transfer_stock(source_key, dest_key, quantity):
                return f"Transferred {quantity} of product {product_id} from store {source_store_id} to store {dest_store_id}."
            return f"Transfer failed: insufficient stock at source store."
        except ValueError as e:
            return f"Transfer failed: {e}"

    def remove_product_from_store(self, store_id, product_id):
        key = (store_id, product_id)
        try:
            self.inventory_manager.remove_product_from_store(key)
            return f"Product {product_id} discontinued at store {store_id}."
        except ValueError as e:
            return f"Removal failed: {e}"

    def subscribe_to_low_stock_alerts(self, observer):
        self.inventory_manager.subscribe(observer)