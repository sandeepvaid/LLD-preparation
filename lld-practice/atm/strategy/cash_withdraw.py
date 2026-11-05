from strategy.withdraw_strategy import WithdrawStrategy


class CashWithdraw(WithdrawStrategy):
    def dispense(self, amount, atm):
        print(f"Dispensing ${amount:.2f} in cash.")
