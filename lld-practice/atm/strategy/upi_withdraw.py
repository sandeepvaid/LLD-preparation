from strategy.withdraw_strategy import WithdrawStrategy


class UpiWithdraw(WithdrawStrategy):
    def __init__(self, upi_id: str):
        self.upi_id = upi_id   # extra data goes in constructor, not in dispense()

    def dispense(self, amount, atm):
        print(f"Transferring ${amount:.2f} to UPI ID: {self.upi_id}")
