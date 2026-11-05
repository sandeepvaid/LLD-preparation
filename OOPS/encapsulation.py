# Encapsulation = Data hiding + Controlled access

class BankAccount:
    def __init__(self, account_number, balance):
        self.__account_number = account_number  # Private attribute
        self.__balance = balance  # Private attribute

    @property
    def get_account_number(self):
        return self.__account_number

    def get_balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False
    
# Create an instance of BankAccount
account = BankAccount("123456789", 1000)    
#Here we use @property to access the private attribute __account_number through the public method get_account_number. That's why we don't need to add paranthesis .
print(f"Account Number: {account.get_account_number}")
print(f"Initial Balance: ${account.get_balance()}")