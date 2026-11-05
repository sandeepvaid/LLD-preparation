from abc import ABC, abstractmethod


# PATTERN: State
# PURPOSE: Each concrete state encapsulates behavior for ONE state of the system.
#          The context (public class) holds the current state and delegates all
#          behavior to it. When an action causes a transition, the state itself
#          switches context.state to the next state.
#
# HOW TO USE:
#   1. Identify all states your system can be in  (e.g. Idle, HasMoney, Dispensing)
#   2. Identify all actions the system can perform (e.g. insert_coin, select_item, refund)
#   3. Create one concrete State subclass per state
#   4. In each subclass, implement every action — either do the real work or print
#      "not allowed in this state"


class BaseState(ABC):
    def __init__(self, context):
        # context is always your main public class (e.g. VendingMachine, ATM)
        # access anything on it via self.ctx
        self.ctx = context
