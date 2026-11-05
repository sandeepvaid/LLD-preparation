# ─────────────────────────────────────────────────────────────────
# FRAMEWORK: State + Strategy + Manager + Context
# ─────────────────────────────────────────────────────────────────
#
# STEP 1 — IDENTIFY STATES
#   Ask: "What modes can this system be in, and does behavior
#         change based on which mode it's in?"
#   If yes → State pattern.
#
#   Vending Machine : Idle | HasMoney | Dispensing
#   ATM             : Idle | CardInserted | PINVerified | Dispensing
#   Coffee Machine  : Idle | SelectingDrink | Brewing | Dispensing
#   Elevator        : Idle | Moving | DoorOpen
#   Hotel Room      : Available | Booked | Occupied | Maintenance
#   Order           : Placed | Confirmed | Shipped | Delivered | Cancelled
#
#
# STEP 2 — IDENTIFY THE STRATEGY
#   Ask: "Is there a behavior that can be swapped at runtime?"
#   If yes → Strategy pattern.
#
#   Vending Machine : PaymentStrategy    (Cash | Card | UPI)
#   ATM             : TransactionStrategy (Withdraw | Deposit | Transfer)
#   Coffee Machine  : PaymentStrategy    (Cash | Card)
#   Parking Lot     : PricingStrategy    (Hourly | Flat | VIP)
#   Ride Sharing    : SurgePricingStrategy
#
#   If the problem has no swappable behavior → skip Strategy.
#   Elevator, Traffic Light → no Strategy needed.
#
#
# STEP 3 — IDENTIFY THE MANAGER
#   Ask: "Does this system manage a collection of things?"
#   If yes → Manager pattern.
#
#   Vending Machine : InventoryManagement  (slots)
#   ATM             : CashManagement       (denominations)
#   Coffee Machine  : IngredientManagement (coffee, milk, sugar)
#   Parking Lot     : SpotManagement       (spots by type)
#   Hotel           : RoomManagement       (rooms by type)
#
#
# STEP 4 — BUILD THE CONTEXT
#   The context (main public class) is the ONLY class that:
#     - knows all states and holds the current one
#     - holds the current strategy
#     - holds the manager
#     - exposes public actions → delegates to self.state
#     - exposes manager wrappers → states talk to context, not manager
#
#
# ─────────────────────────────────────────────────────────────────
# DECISION TABLE — what pattern does each problem need?
# ─────────────────────────────────────────────────────────────────
#
# Problem               State   Strategy   Manager    New pattern needed
# ──────────────────────────────────────────────────────────────────────
# Vending Machine         ✓        ✓          ✓       —
# Coffee Machine          ✓        ✓          ✓       —  (same skeleton)
# ATM                     ✓        ✓          ✓       —  (same skeleton)
# Hotel Booking           ✓        ✓          ✓       —  (same skeleton)
# Parking Lot             ✓        ✓          ✓       Observer (notify on free spot)
# Elevator                ✓        ✗          ✓       —
# Traffic Light           ✓        ✗          ✗       —  (pure state)
# Order Management        ✓        ✗          ✗       Observer (notify on status change)
# Library System          ✗        ✓          ✓       Observer (notify on book return)
# Ride Sharing (Uber)     ✓        ✓          ✓       Observer (match driver/rider)
#
#
# ─────────────────────────────────────────────────────────────────
# RECOMMENDED LEARNING ORDER (for interview efficiency)
# ─────────────────────────────────────────────────────────────────
#
# Round 1 — Same skeleton, just different states/strategies (do these fast):
#   1. Vending Machine  ✅ done
#   2. ATM              → same pattern, adds security states (PIN, card)
#   3. Coffee Machine   → same pattern, adds ingredient management
#
# Round 2 — Introduces Observer pattern (notify other objects on state change):
#   4. Parking Lot      → State + Strategy + Manager + Observer
#   5. Order Management → State + Observer
#
# Round 3 — Complex coordination (multiple contexts talking to each other):
#   6. Ride Sharing     → State + Strategy + Observer across Driver & Rider
#
# Observer pattern (needed in Round 2) in one line:
#   When an object changes state, it calls notify() on a list of
#   subscribers. They each get the update and react.
#   Example: when a parking spot becomes free → notify waiting cars.
