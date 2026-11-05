# whenever our system looks like it has multiple states, and the behavior of the system changes based on the current state, we can use the State pattern to manage these states and their associated behaviors

#Framework we can use everywhere where we use state pattern

#First we create a state class that contains all the different behaviors that we want to implement for each state. This class will be an abstract base class (ABC) that defines the interface for the different states.
from abc import ABC, abstractmethod
class State(ABC):

    def __init__(self,curr_state):
        self.curr_state = curr_state

    @abstractmethod
    def insert_coin(self):
        pass

    @abstractmethod
    def select_item(self):
        pass

    @abstractmethod
    def refund(self):
        pass   

#Now based on these methods how they actully behave in differen states we create a class for that

class IdleState(State):
    def insert_coin(self,amount):
        self.curr_state.balance += amount
        print(f"Inserted ${amount:.2f}. Current balance: ${self.curr_state.balance:.2f}")
        self.curr_state.state = self.curr_state.has_money_state

    def select_item(self):
        print("Please insert a coin first")

    
    def refund(self):
        print("No coin to refund")

class HasMoneyState(State):
    def insert_coin(self,amount):
        self.curr_state.balance += amount
        print(f"Inserted ${amount:.2f}. Current balance: ${self.curr_state.balance:.2f}")
        

    def select_item(self,code):
        if code not in self.curr_state.items:
            print("Invalid item code")
            return
        item = self.curr_state.items[code]
        if item['qty'] <= 0:
            print(f"Sorry, {item['name']} is out of stock.")
            return
        if self.curr_state.balance < item['price']:
            print(f"Insufficient balance. Please insert ${item['price'] - self.curr_state.balance:.2f} more.")
            return
        self.curr_state.state = self.curr_state.dispensing_state
        self.curr_state.state._dispense_item(code)
    def refund(self):
        self.curr_state.balance = 0
        print("Refunded all coins. Current balance: $0.00")

class DispensingState(State):
    def insert_coin(self):
        print("Currently dispensing an item. Please wait.")        

    def select_item(self,code):
        print(f"Dispensing item {code}. Enjoy your {self.curr_state.items[code]['name']}!")

    def _dispense_item(self,code):
        item = self.curr_state.items[code]
        change = self.curr_state.balance - item['price']
        item['qty'] -= 1
        self.curr_state.balance -= item['price']
        print(f"Dispensing {item['name']}. Change returned: ${change:.2f}")
        self.curr_state.state = self.curr_state.idle_state   # back to idle

    def refund(self):
        print("can't refund item is dispensing")


class VendingMachine:
    def __init__(self):
        #define variable for all the states 
        self.idle_state = IdleState(self)
        self.has_money_state = HasMoneyState(self)
        self.dispensing_state = DispensingState(self)
        self.state = self.idle_state
        self.balance = 0
        self.items = {
            "A1": {"name": "Coke",  "price": 1.5, "qty": 5},
            "B2": {"name": "Chips", "price": 2.0, "qty": 3},
        }

    def insert_coin(self, amount):
        self.state.insert_coin(amount)
    
    def refund(self):
        self.state.refund()

    def select_item(self, code):
        self.state.select_item(code)



vm = VendingMachine()
vm.insert_coin(2)
vm.select_item("A1")
vm.insert_coin(1)
vm.select_item("B2")
vm.refund()