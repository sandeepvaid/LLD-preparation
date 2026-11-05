from atm import ATM
from strategy.cash_withdraw import CashWithdraw
from strategy.upi_withdraw import UpiWithdraw

atm = ATM()

print("=== Cash Withdrawal Flow ===")
atm.insert_card("1234")
atm.enter_pin("0000")
atm.view_balance()
atm.withdraw(1000, CashWithdraw())
atm.view_balance()
atm.eject_card()

print("\n=== UPI Withdrawal Flow ===")
atm.insert_card("5678")
atm.enter_pin("1111")
atm.withdraw(500, UpiWithdraw("user@upi"))
atm.eject_card()

print("\n=== Wrong PIN Flow ===")
atm.insert_card("1234")
atm.enter_pin("9999")
atm.enter_pin("9999")
atm.enter_pin("9999")

print("\n=== Action blocked in wrong state ===")
atm.withdraw(100, CashWithdraw())
