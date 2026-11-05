from payment.payment_strategy import PaymentStrategy


class CreditCardPayment(PaymentStrategy):
    def pay(self, amount, vending_machine):
        print(f"Paying ${amount:.2f} with credit card")
        vending_machine.insert_coin(amount)

    def refund(self, amount, vending_machine):
        print(f"Refunding ${amount:.2f} to credit card")

    def cancel(self):
        print("Credit card payment cancelled")
