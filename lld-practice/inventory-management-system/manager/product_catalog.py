import threading

from models.product import Product


class ProductCatalog:
    def __init__(self):
        self.products = {}      # product_id -> Product
        self.key_lock = {}      # product_id -> Lock, created on demand
        self.global_lock = threading.Lock()

    def get_key_lock(self, key):
        if key in self.key_lock:
            return self.key_lock[key]
        with self.global_lock:
            if key not in self.key_lock:
                self.key_lock[key] = threading.Lock()
            return self.key_lock[key]

    def get_product(self, product_id):
        return self.products.get(product_id)

    def create_product(self, product_id, name, price):
        key_lock = self.get_key_lock(product_id)
        with key_lock:
            if product_id in self.products:
                raise ValueError(f"product {product_id} already exists in catalog")
            self.products[product_id] = Product(product_id, name, price)
