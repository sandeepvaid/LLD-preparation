from abc import ABC, abstractmethod


# PATTERN: Strategy
# PURPOSE: Swap algorithms/behaviors at runtime without changing the caller.
#          The context holds a reference to the current strategy and delegates
#          to it. The strategy receives the context so it can update state/balance.
#
# HOW TO USE:
#   1. Identify the behavior that changes (e.g. payment method, pricing, sorting)
#   2. Create an abstract BaseStrategy with one main method
#   3. Create one concrete Strategy subclass per variant
#   4. The context exposes choose_strategy(strategy) to switch at runtime
#
# RULE: Strategy should NOT hold context at construction time.
#       Pass context into the method call instead — keeps strategies reusable
#       across different context instances.


class BaseStrategy(ABC):

    @abstractmethod
    def execute(self, amount, context):
        # amount  → the value being processed (payment amount, discount value, etc.)
        # context → the main public class, so strategy can call context.insert_coin() etc.
        pass
