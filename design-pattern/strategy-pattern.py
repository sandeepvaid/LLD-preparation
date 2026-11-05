from abc import ABC, abstractmethod
#Strategy pattern is a pattern that help us to implement different implementation for any specific process
class PaymentStrategy(ABC):

    @abstractmethod
    def pay(self, amount):
        pass

    @abstractmethod
    def refund(self, amount):
        pass
    
    @abstractmethod
    def cancel(self):
        pass


class CashPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paying ${amount:.2f} in cash")

    def refund(self, amount):
        print(f"Refunding ${amount:.2f} in cash")

    def cancel(self):
        print("Cash payment cancelled")

class CreditCardPayment(PaymentStrategy):   
    def pay(self, amount):
        print(f"Paying ${amount:.2f} with credit card")

    def refund(self, amount):
        print(f"Refunding ${amount:.2f} to credit card")

    def cancel(self):
        print("Credit card payment cancelled")
    

class VendingMachine:
    def __init__(self,payment:PaymentStrategy):
        self.payment = payment
    
    def buy(self,amount):
        self.payment.pay(amount)

    def refund(self,amount):
        self.payment.refund(amount) 


vm = VendingMachine(CashPayment())
vm.buy(2.5)
vm.refund(2.5)  