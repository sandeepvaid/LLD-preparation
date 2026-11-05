from vending_machine import VendingMachine
from payment.cash_payment import CashPayment
from payment.credit_card_payment import CreditCardPayment

vm = VendingMachine()
vm.choose_payment_strategy_and_pay(CashPayment(), 2.5)
vm.select_item("A1")

vm.choose_payment_strategy_and_pay(CreditCardPayment(), 3.0)
vm.select_item("B2")
