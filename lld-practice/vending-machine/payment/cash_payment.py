from payment.payment_strategy import PaymentStrategy


class CashPayment(PaymentStrategy):
    def pay(self, amount, vending_machine):
        print(f"Paying ${amount:.2f} in cash")
        vending_machine.insert_coin(amount)

    def refund(self, amount, vending_machine):
        print(f"Refunding ${amount:.2f} in cash")

    def cancel(self):
        print("Cash payment cancelled")
