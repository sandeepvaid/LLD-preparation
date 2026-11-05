
import threading
from models.inventory import Inventory 

class InventoryManager:
    def __init__(self):
        self.inventory = {}
        self.key_lock ={}
        self.global_lock = threading.Lock()
        self.observers = []

    def subscribe(self, observer):
        self.observers.append(observer)

    def get_key_lock(self,key):
        if key in self.key_lock:
            return self.key_lock[key]
        with self.global_lock:
            if key not in self.key_lock:
                self.key_lock[key] = threading.Lock()
            return self.key_lock[key]
         

    def get_inventory(self,key):
        if key in self.inventory:
            return self.inventory[key]
        else:
            return None
        
    def add_stock(self,key,qty):
       record = self.get_inventory(key)
       if record is None:
           raise ValueError(f"product {key[1]} not onboarded at store {key[0]}")
       return self.inventory[key].add(qty)

    def deduct_stock(self,key,qty):
        record = self.get_inventory(key)
        if record is None:
            raise ValueError(f"product {key[1]} not onboarded at store {key[0]}")
        return self.inventory[key].deduct(qty)

    def remove_product_from_store(self,key):
        record = self.get_inventory(key)
        if record is None:
            raise ValueError(f"product {key[1]} not onboarded at store {key[0]}")
        record.deactivate()

    def transfer_stock(self,source_key,dest_key,qty):
        #acquire the inventory object
        source_inventory = self.get_inventory(source_key)
        dest_inventory = self.get_inventory(dest_key)

        if source_inventory is None:
            raise ValueError(f"product {source_key[1]} not onboarded at store {source_key[0]}")
        if dest_inventory is None:
            raise ValueError(f"product {dest_key[1]} not onboarded at store {dest_key[0]}")

        #Now we can acquire the locks for both source and destination inventory objects in a consistent order to avoid deadlocks
        _, first_obj = min((source_key, source_inventory), (dest_key, dest_inventory))
        _, second_obj = max((source_key, source_inventory), (dest_key, dest_inventory))

        with first_obj._lock:
            with second_obj._lock:
                if not source_inventory.is_active:
                    raise ValueError(f"product {source_key[1]} at store {source_key[0]} is discontinued")
                if not dest_inventory.is_active:
                    raise ValueError(f"product {dest_key[1]} at store {dest_key[0]} is discontinued")
                if source_inventory.quantity >= qty:
                    source_inventory.deduct(qty)
                    dest_inventory.add(qty)
                    return True
                else:
                    return False

    def add_inventory(self,store_id, product_id, quantity,low_stock_threshold=5):
        key = (store_id, product_id)
        key_lock = self.get_key_lock(key)
        with key_lock:
            if key in self.inventory:
                raise ValueError(f"product {product_id} already onboarded at store {store_id}")
            else:
                self.inventory[key] = Inventory(product_id, store_id, quantity, low_stock_threshold, observers=self.observers)