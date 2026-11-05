from models.account import Account


class CardService:
    def __init__(self):
        # in production this talks to the bank's backend API
        self._accounts = {
            "1234": Account("1234", "0000", 5000.0),
            "5678": Account("5678", "1111", 2000.0),
        }

    def verify_card(self, card_number: str) -> bool:
        return card_number in self._accounts

    def verify_pin(self, card_number: str, pin: str) -> bool:
        account = self._accounts.get(card_number)
        return account is not None and account.pin == pin

    def get_balance(self, card_number: str) -> float:
        account = self._accounts.get(card_number)
        return account.balance if account else 0.0

    def deduct(self, card_number: str, amount: float) -> bool:
        account = self._accounts.get(card_number)
        if account is None or account.balance < amount:
            print("Insufficient funds.")
            return False
        account.balance -= amount
        return True
