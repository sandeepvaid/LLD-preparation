# LLD Interview Revision — Night Before Cheat Sheet

Quick-scan reference. Code is Python, kept minimal on purpose — enough to talk through on a whiteboard, not production-grade.

---

## 1. How to Run the Interview (first 2 minutes matter most)

1. **Clarify scope out loud.** Restate the problem, ask 3-5 questions before writing anything:
   - Who are the actors/users?
   - What are the core use cases (list them, prioritize top 4-5)?
   - Scale/concurrency expectations? Single process or distributed?
   - Any explicit extensibility requirement ("should support adding X later")?
2. **List entities (nouns) and actions (verbs).** Nouns → classes. Verbs → methods.
3. **Identify relationships** — is-a (inheritance), has-a (composition/aggregation), uses-a (dependency).
4. **Run it through the framework below** (State / Strategy / Manager / Context) to decide which patterns apply — don't force patterns that aren't needed.
5. **Draw/describe the class diagram** before coding — interfaces first, concrete classes second.
6. **Code the core flow only.** Skip getters/setters unless asked. Narrate as you type.
7. **Close with:** extensibility ("if we add Y tomorrow, only this class changes"), edge cases, and — if asked — concurrency/thread-safety.

**Signal words → pattern:**
| Interviewer says | Think |
|---|---|
| "different types of X behave differently" | Strategy or Inheritance |
| "system has modes/phases" | State |
| "notify others when something changes" | Observer |
| "build up a complex object step by step" | Builder |
| "only one instance ever" | Singleton |
| "wrap/add behavior without changing the class" | Decorator |
| "incompatible interfaces need to talk" | Adapter |
| "undo/redo, queue of actions" | Command |
| "pass request through handlers until one handles it" | Chain of Responsibility |

---

## 2. Personal Framework: State + Strategy + Manager + Context

*(carried over from `framework/HOW_TO_APPLY.py`)*

**Step 1 — States?** "Does behavior change based on which mode the system is in?" → State pattern.
Examples: Vending Machine (Idle/HasMoney/Dispensing), ATM (Idle/CardInserted/PINVerified), Elevator (Idle/Moving/DoorOpen), Order (Placed/Shipped/Delivered).

**Step 2 — Strategy?** "Is there a behavior swappable at runtime?" → Strategy pattern.
Examples: Payment (Cash/Card/UPI), Parking pricing (Hourly/Flat/VIP), Rate limiting (TokenBucket/FixedWindow), Splitwise (Equal/Exact/Percent split).
No swappable behavior → skip it (e.g. Elevator, Traffic Light don't need Strategy).

**Step 3 — Manager?** "Does the system manage a collection of things (spots, slots, rooms, cash)?" → Manager class that owns lookup/allocation logic, separate from the context.

**Step 4 — Context (the main public class):**
- Holds current state + all state objects
- Holds current strategy
- Holds the manager
- Public methods only delegate to `self.state.*` — states call back into context, never touch the manager directly (keeps a single source of truth).

**Decision table:**
| Problem | State | Strategy | Manager | Extra pattern |
|---|---|---|---|---|
| Vending Machine ✅ | ✓ | ✓ | ✓ | — |
| ATM ✅ | ✓ | ✓ | ✓ | — |
| Parking Lot ✅ | — | ✓ | ✓ | Observer (notify on free spot) |
| Elevator | ✓ | ✗ | ✓ | — |
| Order Management | ✓ | ✗ | ✗ | Observer (status change) |
| Library System | ✗ | ✓ | ✓ | Observer (book returned) |
| Ride Sharing | ✓ | ✓ | ✓ | Observer (match driver/rider) |
| Splitwise | ✗ | ✓ | ✓ | — |
| Rate Limiter | ✗ | ✓ | ✓ | — |

---

## 3. OOP Fundamentals

- **Encapsulation** — bundle data + methods, hide internal state behind an interface (`_private`/property in Python).
- **Abstraction** — expose *what* an object does, hide *how* (ABC / interface).
- **Inheritance** — "is-a" relationship, reuse via subclassing. Prefer composition when it's not a true is-a.
- **Polymorphism** — same interface, different behavior at runtime (method overriding + duck typing in Python).

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14159 * self.r ** 2

class Square(Shape):
    def __init__(self, side): self.side = side
    def area(self): return self.side ** 2

for shape in [Circle(2), Square(3)]:
    print(shape.area())   # polymorphism — caller doesn't know/care which subclass
```

---

## 4. SOLID + DRY

| Principle | One-liner |
|---|---|
| **S**ingle Responsibility | A class should have exactly one reason to change. |
| **O**pen/Closed | Open for extension, closed for modification — add new subclasses, don't edit existing ones. |
| **L**iskov Substitution | A subclass must be substitutable for its base class without breaking correctness. |
| **I**nterface Segregation | Prefer many small, focused interfaces over one fat interface clients don't fully use. |
| **D**ependency Inversion | Depend on abstractions, not concrete classes — inject dependencies. |
| **DRY** | Don't repeat logic — extract shared behavior once. |

**OCP — bad vs good** *(matches `design-principle/open-close-principle.py`)*:
```python
# BAD — every new payment type means editing this method
class PaymentProcessor:
    def process(self, payment_type, amount):
        if payment_type == "credit_card": ...
        elif payment_type == "paypal": ...
        else: raise ValueError("unsupported")

# GOOD — extend via new subclass, never touch existing code
class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount): ...

class CreditCardProcessor(PaymentProcessor):
    def process(self, amount): print(f"credit card: {amount}")

class PayPalProcessor(PaymentProcessor):
    def process(self, amount): print(f"paypal: {amount}")
```

**LSP violation example** (common interview gotcha — Square extends Rectangle):
```python
class Rectangle:
    def set_width(self, w): self.width = w
    def set_height(self, h): self.height = h

class Square(Rectangle):          # BAD: breaks LSP
    def set_width(self, w): self.width = self.height = w   # silently changes height too
```
Fix: don't model Square as a Rectangle subclass; both implement a `Shape` interface instead.

**DIP example:**
```python
# BAD — high-level class depends on a concrete low-level class
class MySQLDatabase:
    def save(self, data): ...

class UserService:
    def __init__(self):
        self.db = MySQLDatabase()   # tightly coupled

# GOOD — depend on abstraction, inject the implementation
class Database(ABC):
    @abstractmethod
    def save(self, data): ...

class UserService:
    def __init__(self, db: Database):
        self.db = db   # can swap MySQL/Postgres/Mock without touching UserService
```

---

## 5. UML Quick Reference

| Relationship | Symbol | Meaning | Example |
|---|---|---|---|
| Inheritance (is-a) | `▷——` hollow triangle | Subclass extends base | `Car ▷—— Vehicle` |
| Realization (implements) | `▷- - -` dashed hollow triangle | Class implements interface | `Car ▷- - - Drivable` |
| Composition (owns, lifecycle-bound) | `◆——` filled diamond | Part can't exist without whole | `Engine ◆—— Car` |
| Aggregation (has-a, independent lifecycle) | `◇——` hollow diamond | Part can exist without whole | `Wheel ◇—— Car`* |
| Association | `——` plain line | General "uses/knows about" | `Driver —— Car` |
| Dependency | `- - >` dashed arrow | Temporary use (method param/local var) | `OrderService - -> EmailSender` |

*Multiplicity notation: `1`, `0..1`, `*` (many), `1..*` — write at each end of the line, e.g. `ParkingLot 1 —— * ParkingSpot`.

Rule of thumb when explaining to interviewer: **composition = "dies with parent"** (Room ◆ House — destroy house, room is gone). **Aggregation = "can outlive parent"** (Book ◇ Library — remove library record, book still physically exists).

---

## 6. Design Pattern Catalog

### Creational

**Singleton** — exactly one instance, global access point.
```python
class ConfigManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```
Thread-safe version needs a lock around instance creation (see §7).

**Factory Method** — delegate object creation to subclasses/a method, caller doesn't `new` concrete classes directly.
```python
class VehicleFactory:
    @staticmethod
    def create(vehicle_type: str):
        return {"car": Car, "truck": Truck, "motorcycle": Motorcycle}[vehicle_type]()
```
Used in your parking-lot code implicitly wherever a `Vehicle` subclass is instantiated by type.

**Builder** — construct a complex object step by step, avoid telescoping constructors.
```python
class Pizza:
    def __init__(self): self.toppings = []

class PizzaBuilder:
    def __init__(self): self.pizza = Pizza()
    def add_topping(self, t): self.pizza.toppings.append(t); return self
    def build(self): return self.pizza

pizza = PizzaBuilder().add_topping("cheese").add_topping("olives").build()
```

**Prototype** — clone an existing object instead of building from scratch.
```python
import copy
class Prototype:
    def clone(self): return copy.deepcopy(self)
```

### Structural

**Adapter** — convert one interface into another the client expects.
```python
class LegacyPrinter:
    def print_old(self, text): print(f"[legacy] {text}")

class ModernPrinterInterface(ABC):
    @abstractmethod
    def print(self, text): ...

class PrinterAdapter(ModernPrinterInterface):
    def __init__(self, legacy: LegacyPrinter): self.legacy = legacy
    def print(self, text): self.legacy.print_old(text)
```

**Decorator** — attach new behavior to an object dynamically without touching its class.
```python
class Coffee(ABC):
    @abstractmethod
    def cost(self): ...

class SimpleCoffee(Coffee):
    def cost(self): return 2.0

class MilkDecorator(Coffee):
    def __init__(self, coffee: Coffee): self.coffee = coffee
    def cost(self): return self.coffee.cost() + 0.5

coffee = MilkDecorator(SimpleCoffee())
print(coffee.cost())  # 2.5
```

**Facade** — one simple interface hiding a complex subsystem.
```python
class Facade:
    def __init__(self): self.cpu, self.memory, self.disk = CPU(), Memory(), Disk()
    def start_computer(self):
        self.cpu.boot(); self.memory.load(); self.disk.read()
```

**Composite** — treat individual objects and groups of objects uniformly (tree structure).
```python
class FileSystemNode(ABC):
    @abstractmethod
    def size(self): ...

class File(FileSystemNode):
    def __init__(self, size): self._size = size
    def size(self): return self._size

class Folder(FileSystemNode):
    def __init__(self): self.children = []
    def add(self, node): self.children.append(node)
    def size(self): return sum(c.size() for c in self.children)
```

**Proxy** — stand-in that controls access to the real object (lazy load, caching, access control).
```python
class RealImage:
    def __init__(self, path): self.path = path; print(f"loading {path}")
    def display(self): print(f"showing {self.path}")

class ProxyImage:
    def __init__(self, path): self.path = path; self._real = None
    def display(self):
        if self._real is None: self._real = RealImage(self.path)   # lazy load
        self._real.display()
```

### Behavioral

**Strategy** — swap an algorithm/behavior at runtime via composition. *(you already have this in `design-pattern/strategy-pattern.py`)*

**State** — object changes behavior when its internal state changes; each state is its own class. *(you already have this in `design-pattern/state-pattern.py`)*

**Observer** — one-to-many dependency; subscribers get notified when the subject changes.
```python
class Subject:
    def __init__(self): self._observers = []
    def subscribe(self, obs): self._observers.append(obs)
    def notify(self, event): 
        for obs in self._observers: obs.update(event)

class ParkingSpot(Subject):
    def free_up(self):
        self.notify("spot_available")

class WaitingCar:
    def update(self, event): print(f"notified: {event}")
```

**Command** — encapsulate a request as an object (enables undo/redo, queuing, logging).
```python
class Command(ABC):
    @abstractmethod
    def execute(self): ...
    @abstractmethod
    def undo(self): ...

class LightOnCommand(Command):
    def __init__(self, light): self.light = light
    def execute(self): self.light.on()
    def undo(self): self.light.off()
```

**Chain of Responsibility** — pass a request along a chain of handlers until one handles it.
```python
class Handler(ABC):
    def __init__(self): self.next = None
    def set_next(self, h): self.next = h; return h
    @abstractmethod
    def handle(self, request): ...

class ManagerApproval(Handler):
    def handle(self, amount):
        if amount <= 1000: print("approved by manager")
        elif self.next: self.next.handle(amount)
        else: print("rejected")
```

**Template Method** — base class defines the skeleton of an algorithm, subclasses fill in steps.
```python
class DataProcessor(ABC):
    def process(self):           # template method — fixed sequence
        self.read(); self.transform(); self.write()
    @abstractmethod
    def read(self): ...
    @abstractmethod
    def transform(self): ...
    def write(self): print("writing output")   # shared default step
```

**Iterator** — sequentially access elements of a collection without exposing its structure. (Python's `__iter__`/`__next__` protocol *is* this pattern.)

**Mediator** — centralize how a set of objects interact, so they don't reference each other directly.
```python
class ChatRoom:
    def send(self, sender, message):
        print(f"[{sender}]: {message}")   # users talk through the room, not to each other

class User:
    def __init__(self, name, room): self.name, self.room = name, room
    def send(self, message): self.room.send(self.name, message)
```

**Visitor** — add new operations to a class hierarchy without modifying the classes (double dispatch). Rarely needed in interviews unless explicitly asked — mention it exists, don't over-invest.

---

## 7. Concurrency Considerations (if asked)

- **Thread-safe Singleton:**
```python
import threading
class Singleton:
    _instance = None
    _lock = threading.Lock()
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:      # double-checked locking
                    cls._instance = super().__new__(cls)
        return cls._instance
```
- **Guarding shared mutable state** (e.g. parking spot allocation, ticket counters): wrap critical sections with `threading.Lock()`, keep the locked region as small as possible.
- **Producer-consumer:** `queue.Queue` is already thread-safe — use it instead of hand-rolled locking when the problem is "one thing feeds another."
- Call out **where race conditions could occur** even if you don't code the fix: e.g. "two threads calling `enter_vehicle` simultaneously could both grab the same spot — I'd lock around `find_spot_for_vehicle` + `park_vehicle`."
- Prefer **atomic operations / optimistic concurrency (compare-and-swap)** over broad locks when interviewer pushes on scale.

---

## 8. Already Practiced — Quick Recap

*(full code in `lld-practice/`)*

- **Vending Machine** (`vending-machine/`) — State (Idle → HasMoney → Dispensing) + Strategy (Cash/Card payment) + Manager (`InventoryManagement` over item slots).
- **ATM** (`atm/`) — State (Idle → CardInserted → Transaction) + Strategy (Cash/UPI withdraw) + `CardService` acting as the manager; states never touch the service directly, always via the context (`ATM`) — good example of keeping a single source of truth.
- **Parking Lot** (`parking-lot/`) — Strategy (`FareCalculator`: base/peak-hours pricing) + Manager (`ParkingManager` allocates `ParkingSpot` by `VehicleSize`) + `Ticket` as a value object. No State needed here since a parking lot doesn't have global modes. Add Observer if asked to "notify waiting cars when a spot frees up."

---

## 9. New Worked Problems

### 9.1 Elevator System
State (per elevator) + Manager (controller dispatches to best elevator). No Strategy needed.

```python
from enum import Enum
from abc import ABC, abstractmethod

class Direction(Enum):
    UP, DOWN, IDLE = 1, -1, 0

class ElevatorState(ABC):
    def __init__(self, elevator): self.elevator = elevator
    @abstractmethod
    def request_floor(self, floor): ...
    @abstractmethod
    def step(self): ...

class IdleState(ElevatorState):
    def request_floor(self, floor):
        e = self.elevator
        e.add_destination(floor)
        e.state = e.moving_state
    def step(self): pass

class MovingState(ElevatorState):
    def request_floor(self, floor): self.elevator.add_destination(floor)
    def step(self):
        e = self.elevator
        if e.current_floor == e.next_destination():
            e.state = e.door_open_state
        else:
            e.current_floor += e.direction.value

class DoorOpenState(ElevatorState):
    def request_floor(self, floor): self.elevator.add_destination(floor)
    def step(self):
        e = self.elevator
        e.destinations.pop(0)
        e.state = e.idle_state if not e.destinations else e.moving_state

class Elevator:
    def __init__(self, id):
        self.id, self.current_floor = id, 0
        self.direction, self.destinations = Direction.IDLE, []
        self.idle_state, self.moving_state, self.door_open_state = (
            IdleState(self), MovingState(self), DoorOpenState(self))
        self.state = self.idle_state

    def add_destination(self, floor):
        if floor not in self.destinations:
            self.destinations.append(floor); self.destinations.sort()
        self.direction = Direction.UP if floor > self.current_floor else Direction.DOWN

    def next_destination(self): return self.destinations[0]
    def step(self): self.state.step()

class ElevatorController:                       # Manager
    def __init__(self, num_elevators):
        self.elevators = [Elevator(i) for i in range(num_elevators)]

    def request_elevator(self, floor):
        best = min(self.elevators, key=lambda e: abs(e.current_floor - floor))
        best.state.request_floor(floor)
        return best.id
```
Talking points: dispatch algorithm (nearest-elevator here; real systems use SCAN/LOOK to batch same-direction stops), starvation prevention, multiple simultaneous requests.

### 9.2 Splitwise / Expense Sharing
Strategy for split type + Manager holding a balance ledger with debt simplification.

```python
from abc import ABC, abstractmethod
from collections import defaultdict

class User:
    def __init__(self, id, name): self.id, self.name = id, name

class Split:
    def __init__(self, user, amount=0): self.user, self.amount = user, amount

class SplitStrategy(ABC):
    @abstractmethod
    def compute(self, total, splits): ...

class EqualSplitStrategy(SplitStrategy):
    def compute(self, total, splits):
        share = total / len(splits)
        for s in splits: s.amount = share

class ExactSplitStrategy(SplitStrategy):
    def compute(self, total, splits):
        assert abs(sum(s.amount for s in splits) - total) < 1e-6

class PercentSplitStrategy(SplitStrategy):
    def compute(self, total, splits):
        assert sum(s.amount for s in splits) == 100
        for s in splits: s.amount = total * s.amount / 100

class Expense:
    def __init__(self, paid_by, amount, splits, strategy: SplitStrategy):
        strategy.compute(amount, splits)
        self.paid_by, self.amount, self.splits = paid_by, amount, splits

class ExpenseManager:                            # Manager
    def __init__(self):
        self.balances = defaultdict(lambda: defaultdict(float))  # balances[a][b] = a owes b

    def add_expense(self, expense: Expense):
        for split in expense.splits:
            if split.user == expense.paid_by: continue
            self.balances[split.user][expense.paid_by] += split.amount
            self._simplify(split.user, expense.paid_by)

    def _simplify(self, a, b):
        net = self.balances[a][b] - self.balances[b][a]
        self.balances[a][b] = max(net, 0)
        self.balances[b][a] = max(-net, 0)

    def show_balances(self, user):
        for other, amt in self.balances[user].items():
            if amt > 0: print(f"{user.name} owes {other.name}: {amt:.2f}")
```
Talking points: why simplify pairwise vs. global min-cash-flow-graph optimization (greedy max-creditor/max-debtor matching minimizes total transactions across a group — mention it, full impl rarely required).

### 9.3 Rate Limiter
Strategy per algorithm, one instance per user/API key.

```python
import time
from abc import ABC, abstractmethod

class RateLimiterStrategy(ABC):
    @abstractmethod
    def allow_request(self) -> bool: ...

class TokenBucketLimiter(RateLimiterStrategy):
    def __init__(self, capacity, refill_per_sec):
        self.capacity, self.tokens = capacity, capacity
        self.refill_per_sec, self.last_refill = refill_per_sec, time.time()

    def allow_request(self):
        now = time.time()
        self.tokens = min(self.capacity, self.tokens + (now - self.last_refill) * self.refill_per_sec)
        self.last_refill = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

class FixedWindowLimiter(RateLimiterStrategy):
    def __init__(self, max_requests, window_seconds):
        self.max_requests, self.window = max_requests, window_seconds
        self.count, self.window_start = 0, time.time()

    def allow_request(self):
        now = time.time()
        if now - self.window_start >= self.window:
            self.window_start, self.count = now, 0
        if self.count < self.max_requests:
            self.count += 1
            return True
        return False

class RateLimiter:                               # Manager, keyed per user
    def __init__(self): self.user_limiters = {}
    def register(self, user_id, strategy: RateLimiterStrategy): self.user_limiters[user_id] = strategy
    def is_allowed(self, user_id) -> bool: return self.user_limiters[user_id].allow_request()
```
Talking points: fixed window's burst-at-boundary problem → sliding window log/counter fixes it; token bucket allows short bursts up to capacity; distributed rate limiting needs shared state (Redis) instead of in-process counters.

### 9.4 Tic-Tac-Toe (generalizes to Connect-4-style N x N)
Plain OOP, win-check as Strategy so it can extend to different board sizes/win-lengths.

```python
from abc import ABC, abstractmethod

class Board:
    def __init__(self, size=3):
        self.size = size
        self.grid = [[None] * size for _ in range(size)]

    def place(self, row, col, symbol):
        if self.grid[row][col] is not None: raise ValueError("cell occupied")
        self.grid[row][col] = symbol

    def is_full(self): return all(c is not None for row in self.grid for c in row)

class Player:
    def __init__(self, name, symbol): self.name, self.symbol = name, symbol

class WinningStrategy(ABC):
    @abstractmethod
    def check_winner(self, board, row, col, symbol) -> bool: ...

class LineWinningStrategy(WinningStrategy):
    def check_winner(self, board, row, col, symbol):
        n, g = board.size, board.grid
        if all(g[row][c] == symbol for c in range(n)): return True
        if all(g[r][col] == symbol for r in range(n)): return True
        if row == col and all(g[i][i] == symbol for i in range(n)): return True
        if row + col == n - 1 and all(g[i][n - 1 - i] == symbol for i in range(n)): return True
        return False

class TicTacToeGame:
    def __init__(self, players, board_size=3, strategy=None):
        self.board, self.players = Board(board_size), players
        self.turn, self.winner = 0, None
        self.strategy = strategy or LineWinningStrategy()

    def play(self, row, col):
        player = self.players[self.turn]
        self.board.place(row, col, player.symbol)
        if self.strategy.check_winner(self.board, row, col, player.symbol):
            self.winner = player
            return
        self.turn = (self.turn + 1) % len(self.players)
```
Talking points: same skeleton scales to Chess (Piece hierarchy + polymorphic `valid_moves()`) — if asked for Chess, swap `symbol` placement for a `Piece` object per square and add per-piece movement rules.

### 9.5 LRU Cache
Not pattern-heavy — the classic "HashMap + Doubly Linked List for O(1) get/put" data-structure design question.

```python
class Node:
    def __init__(self, key, value):
        self.key, self.value = key, value
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity, self.cache = capacity, {}          # key -> Node
        self.head, self.tail = Node(0, 0), Node(0, 0)      # dummies; head-side = most recent
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _add_front(self, node):
        node.next, node.prev = self.head.next, self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.cache: return -1
        node = self.cache[key]
        self._remove(node); self._add_front(node)
        return node.value

    def put(self, key, value):
        if key in self.cache: self._remove(self.cache[key])
        node = Node(key, value)
        self.cache[key] = node
        self._add_front(node)
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
```
Talking points: why not just a list (`O(n)` reordering) or `OrderedDict` (fine in Python, but interviewer usually wants the manual DLL to prove you understand *why* it's O(1)); LFU is the natural follow-up ("what if we evict by frequency instead?").

---

## 10. Common Pitfalls

- Jumping to code before clarifying requirements — costs more time than it saves.
- Over-engineering: adding Strategy/Observer/Factory where a plain `if/else` or single class would do. Justify every pattern with a concrete "what changes if we add X" reason.
- Forgetting the manager/controller layer and cramming allocation logic into the context class.
- Ignoring edge cases out loud: full capacity, invalid input, concurrent access, empty collections.
- Not stating trade-offs — interviewers often care more about *why* you chose an approach than the final code.
- Silence while thinking — narrate, even "let me think about how state transitions work here."

---

## 11. Night-Before Checklist

- [ ] Can explain State vs Strategy vs Observer in one sentence each, with a different example than the one you were taught.
- [ ] Can recite SOLID with one good/bad snippet per principle.
- [ ] Comfortable drawing composition vs aggregation vs inheritance arrows.
- [ ] Can build Vending Machine / ATM / Parking Lot skeleton from memory in under 10 minutes (already practiced — just re-run the framework mentally).
- [ ] Can sketch at least one of: Elevator, Splitwise, Rate Limiter, Tic-Tac-Toe, LRU Cache without looking.
- [ ] Have 3-5 clarifying questions ready to ask before any problem, regardless of what's given.
- [ ] Practiced narrating out loud while coding, not just typing silently.

Good luck tomorrow.
