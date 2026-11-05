# Rate Limiter — LLD Design Doc

Design-first, code-later. This lays out requirements, entities, and the class shape so we agree on the design before writing any implementation.

---

## 1. Requirements

**Functional**
- Given a key (user id / API key / IP), decide whether the current request is `allowed` or `rejected`.
- Support more than one limiting algorithm, swappable per client/API without touching the core system.
- Each key can have its own limit config (e.g. free tier: 10 req/min, paid tier: 1000 req/min).

**Non-functional (to confirm with interviewer/ourselves before building)**
- Single process (in-memory) or distributed (shared state across multiple app servers, e.g. via Redis)?
- Expected request volume — does the check itself need to be lock-free / low-latency?
- What happens on rejection — just a boolean, or do we also return retry-after / remaining-quota info?

> Open questions to settle before coding — flag these back to me when we start:
> 1. In-memory only for now, distributed as a stretch goal?
> 2. Do we need per-key custom limits, or one global limit to start simple?
> 3. Should `is_allowed()` return just `bool`, or a richer result object (`allowed`, `retry_after_seconds`, `remaining`)?

---

## 2. Entities (nouns → classes)

| Entity | Responsibility |
|---|---|
| `RateLimiterStrategy` | Interface — one algorithm's decision logic (`allow_request`) |
| `FixedWindowLimiter` | Concrete strategy |
| `SlidingWindowLogLimiter` | Concrete strategy |
| `SlidingWindowCounterLimiter` | Concrete strategy |
| `TokenBucketLimiter` | Concrete strategy |
| `LeakyBucketLimiter` | Concrete strategy |
| `RateLimiterConfig` | Value object — limit, window size, algorithm choice, per key |
| `RateLimiterRegistry` | Manager — owns one strategy instance per key, creates on first use |
| `RateLimiter` | Context / public entry point — `is_allowed(key)` |

---

## 3. Which pattern applies (per our framework)

- **State?** No — a rate limiter doesn't have global modes that change its own behavior over time. Skip State.
- **Strategy?** Yes — the algorithm (fixed window / sliding window / token bucket / leaky bucket) is exactly a swappable behavior behind one interface. This is the core pattern here.
- **Manager?** Yes — something has to own *one limiter instance per key* (a user shouldn't share a bucket with another user) and hand back the right one on each request. That's `RateLimiterRegistry`.
- **Context?** `RateLimiter` — the only public-facing class. Delegates to the registry to find the right strategy instance, then delegates to the strategy for the actual decision.

So: **Strategy + Manager + Context**, no State — matches the Splitwise/Rate-Limiter row in the framework decision table.

---

## 4. Algorithms to support — tradeoffs

| Algorithm | Idea | Pro | Con |
|---|---|---|---|
| Fixed Window | Count requests in a fixed-size clock-aligned window, reset each window | Simple, O(1) memory per key | Burst at window boundary — 2x limit possible right at the edge |
| Sliding Window Log | Store timestamp of every request, count how many fall in last N seconds | Precise, no boundary burst | O(n) memory per key — stores every timestamp |
| Sliding Window Counter | Weighted average of current + previous fixed window | Good approximation of sliding window, O(1) memory | Slight inaccuracy vs. true sliding log |
| Token Bucket | Bucket refills at fixed rate, request consumes a token | Allows controlled bursts up to bucket capacity | Slightly more state to track (tokens + last refill time) |
| Leaky Bucket | Requests queue and drain at a fixed rate | Smooths bursts into a constant output rate | Requests can be delayed, not just rejected — different semantics |

We'll pick which of these to actually implement together — token bucket + fixed window are usually enough to demonstrate the pattern; sliding window log/counter are good follow-ups if the interviewer pushes on "fixed window has a burst problem."

---

## 5. Class shape (interfaces only — no bodies yet)

```python
from abc import ABC, abstractmethod

class RateLimiterStrategy(ABC):
    @abstractmethod
    def allow_request(self) -> bool: ...

class FixedWindowLimiter(RateLimiterStrategy): ...
class SlidingWindowLogLimiter(RateLimiterStrategy): ...
class TokenBucketLimiter(RateLimiterStrategy): ...

class RateLimiterConfig:
    def __init__(self, max_requests: int, window_seconds: int, algorithm: str):
        ...

class RateLimiterRegistry:               # Manager
    def get_or_create(self, key: str, config: RateLimiterConfig) -> RateLimiterStrategy: ...

class RateLimiter:                       # Context / public entry point
    def __init__(self, registry: RateLimiterRegistry): ...
    def is_allowed(self, key: str) -> bool: ...
```

---

## 6. Extensibility angles to be ready to discuss

- **Adding a new algorithm** → just a new `RateLimiterStrategy` subclass, `RateLimiter`/`RateLimiterRegistry` untouched (OCP).
- **Distributed rate limiting** → swap the in-memory registry's storage for Redis (`INCR` + `EXPIRE` for fixed window, sorted sets for sliding log, Lua script for token bucket) — the `RateLimiterStrategy` interface stays the same, only the internals change.
- **Per-endpoint + per-user limits combined** → key becomes a composite `(user_id, endpoint)`, no structural change needed, just how the registry keys are formed.
- **Thread safety** → each key's strategy instance is mutated on every request; if multi-threaded, guard the read-modify-write inside each strategy with a lock, or make the registry hand out one strategy per (key, thread) — decide based on whether interviewer asks.

---

## Next step

Ready to build — starting point: confirm the 3 open questions in §1, then implement `RateLimiterStrategy` + one concrete strategy (suggest Token Bucket first) + `RateLimiterRegistry` + `RateLimiter`, matching the file layout used in `parking-lot/` and `vending-machine/` (`strategy/`, `manager/`, top-level context file).
