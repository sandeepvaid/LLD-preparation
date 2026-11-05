# PATTERN: Context (Facade / Public Class)
# PURPOSE: The single entry point the outside world interacts with.
#          It wires State + Strategy + Manager together and is the ONLY class
#          that knows about all three layers.
#
# LAYERS:
#   ┌─────────────────────────────────────────────┐
#   │             PUBLIC (caller sees)             │
#   │  action_1()  action_2()  choose_strategy()  │
#   ├─────────────────────────────────────────────┤
#   │         STATE LAYER (delegates to)           │
#   │  self.state.action_1()                       │
#   │  self.state.action_2()                       │
#   ├─────────────────────────────────────────────┤
#   │  MANAGER WRAPPERS  │  STRATEGY WRAPPER       │
#   │  get_item(code)    │  choose_strategy()      │
#   │  remove_item()     │  current_strategy.pay() │
#   └─────────────────────────────────────────────┘
#
# HOW TO USE:
#   1. In __init__: create all state instances (pass self), set self.state = initial_state
#   2. In __init__: create manager instance, seed with initial data
#   3. Each public action just delegates: self.state.action()
#   4. Add thin manager wrappers (get_item, remove_item) so states never
#      reach through to the manager directly
#   5. Add choose_strategy(strategy) to swap payment/pricing at runtime


class BaseContext:
    def __init__(self):
        # --- State layer ---
        # self.idle_state    = IdleState(self)
        # self.active_state  = ActiveState(self)
        # self.state         = self.idle_state      # start state

        # --- Manager layer ---
        # self.manager = ConcreteManager()

        # --- Strategy layer ---
        # self.strategy = None

        pass

    # --- Manager wrappers (Law of Demeter) ---
    # def get_item(self, key):
    #     return self.manager.get(key)
    #
    # def remove_item(self, key, qty):
    #     self.manager.remove_item(key, qty)

    # --- Strategy entry point ---
    # def choose_strategy(self, strategy, amount):
    #     self.strategy = strategy
    #     self.strategy.execute(amount, self)

    # --- Public actions (delegate to current state) ---
    # def action_1(self, ...):
    #     self.state.action_1(...)
    #
    # def action_2(self, ...):
    #     self.state.action_2(...)
