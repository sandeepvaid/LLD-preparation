from abc import ABC, abstractmethod
#Open close principle states that software entities (classes, modules, functions, etc.) should be open for extension but closed for modification. This means that you should be able to add new functionality to a software entity without changing its existing code.

#Example without Open-Closed Principle:
#Here we have a PaymentProcessor class that processes different types of payments. If we want to add a new payment type, we would have to modify the existing code, which can lead to bugs and maintenance issues.
class PaymentProcessor:
    def process_payment(self, payment_type, amount):
        if payment_type == "credit_card":
            print(f"Processing credit card payment of {amount}")
        elif payment_type == "paypal":
            print(f"Processing PayPal payment of {amount}")
        else:
            raise ValueError("Unsupported payment type")
        

#Example with Open-Closed Principle:
#In this refactored example, we define a base class PaymentProcessor and create separate classes for each payment type that inherit from it. This way, we can add new payment types without modifying the existing code, adhering to the Open-Closed Principle.
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        raise NotImplementedError("Subclasses must implement this method")
    
class CreditCardPaymentProcessor(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing credit card payment of {amount}")
    
class PayPalPaymentProcessor(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing PayPal payment of {amount}")
# Now we can easily add new payment types by creating new classes that inherit from PaymentProcessor without modifying the existing code. For example, if we want to add a new payment type for Bitcoin, we can simply create a new class without changing the existing payment processors. This promotes code maintainability and reduces the risk of introducing bugs when adding new features.


p1 = CreditCardPaymentProcessor()
p2 = PayPalPaymentProcessor()

p1.process_payment(100)
p2.process_payment(200)