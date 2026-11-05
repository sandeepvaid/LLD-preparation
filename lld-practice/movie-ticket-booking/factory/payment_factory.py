from ..strategy.payment_strategy import CashPaymentStrategy

class PaymentFactory:
    _registry = {"CashPayment": CashPaymentStrategy}

    def _get(self, strategy_name):
        strategy_class = self._registry.get(strategy_name)
        if not strategy_class:
            raise ValueError(f"Payment strategy '{strategy_name}' not found.")
        return strategy_class()
