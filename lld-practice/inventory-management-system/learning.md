# Inventory Management System — Learning Notes

Concepts to understand and be able to *talk through* before we touch code. Design (`design.md`) and implementation come after this.

---

## 1. Requirements Recap

**This is the authoritative, scoped-down spec** (superseding the earlier looser exploration below it in this doc):

**Functional**
- Manage millions of products.
- Create and update products *inside a store* (i.e., per-store inventory records — onboarding and stock changes).
- Each store is managed by an inventory management system.
- Low-stock alerts.

**Explicitly out of scope**
- Stock transfer between stores/warehouses.
- Check availability — given a product and quantity, return which warehouses can fulfill it (i.e., no cross-store query/routing logic at all).
- **Ordering/checkout itself** — a separate, earlier scope decision: `Order`, cart, and payment belong to a hypothetical external Order/Checkout service, not this system. See §6.
- **Reservation / hold-with-expiry semantics** — an earlier pass explored a full reserve→confirm→release flow with TTL-based holds (relevant if this system fed a cart/checkout flow). Deliberately dropped to keep this build simple and tightly matched to the spec: stock changes are direct (`add_stock`/`deduct_stock`), not claimed-then-committed. Worth knowing the reserve/confirm/release *idea* exists as a follow-up answer (see the retained discussion in §5), even though it's not built.

**Non-functional**
- Thread safety under concurrent operations — this is the requirement the whole exercise has centered on.

**One open design question worth resolving explicitly, not silently**: "each store is managed by an inventory management system" could mean either (a) one centralized `InventoryManager` shared across all stores, keyed by `(store_id, product_id)` — what's actually built so far — or (b) a dedicated `InventoryManager` instance *per store* (each internally keyed by `product_id` alone, since `store_id` would be implicit/fixed per instance). Both are defensible; (b) more literally matches "each store is managed by..." and mirrors a real per-dark-store deployment model. Worth stating both interpretations out loud in an interview and picking one deliberately rather than assuming.

Clarifying questions worth asking out loud before designing:
1. Single process (in-memory) to start, with a note on how it'd extend to multi-server/distributed and to millions of products (same escalation path as Rate Limiter — see §12's lock-striping note, which stops being a hypothetical footnote once "millions of products" is a stated requirement)?
2. Centralized `InventoryManager` vs. one per store (the open question above)?
3. Is soft-delete (discontinuing a product at a store) required, or is create/update sufficient? (Already built either way — see `implementation.md`.)

---

## 2. What's Reused From Before (not re-explained here — see `LLD_INTERVIEW_REVISION.md`)

- **Manager pattern** for owning a collection of stock records → same shape as `InventoryManagement` (vending machine) / `ParkingManager` (parking lot).
- **Registry keyed by identity, created (explicitly, not lazily)** → same *shape* as `RateLimiterRegistry`, keyed by `(store_id, product_id)` instead of client key — though note the create semantics differ (explicit `create_inventory_record`, not lazy `get_or_create` — see the design correction in `implementation.md` §2).
- **Observer** for low-stock alerts → now an explicit functional requirement (§1), not just a nice-to-have — this needs to actually get built, not just discussed as a gap.

**No longer applicable, given the scoped-down requirements**: Strategy for store selection and State for an order lifecycle were both explored earlier in this doc's history, but store selection requires cross-store availability logic (§1: explicitly out of scope) and order lifecycle belongs to the separately-scoped-out Order/Checkout concern (§6). Neither pattern is needed for this system's actual boundary.

The rest of this doc is what's actually *new*.

---

## 3. The Core Problem: Check-and-Decrement Race Condition

The naive version:
```python
if inventory.stock >= quantity:
    inventory.stock -= quantity
    return True
return False
```

This looks fine single-threaded. Under concurrency it's broken — this is a **TOCTOU bug** (Time-Of-Check to Time-Of-Use): two threads can both read `stock = 5`, both see `5 >= 5` as true for a quantity-5 order, both proceed to subtract, and you've sold 10 units of something you had 5 of.

**Why this matters more here than in Parking Lot**: a parking spot double-booking is a minor UX annoyance (redirect the second car). Overselling inventory is a business-correctness problem — you've promised something you can't deliver. Say this distinction out loud if asked "how is this different from what you built before."

---

## 4. Pessimistic vs Optimistic Concurrency Control

Two families of fix — know both, and know when you'd pick each.

**Pessimistic locking** — grab a lock *before* touching the data, hold it through the whole check-and-decrement, release after.
```python
with self.lock:                      # one lock per (store_id, product_id)
    if inventory.stock >= quantity:
        inventory.stock -= quantity
        return True
    return False
```
- Simple to reason about, guarantees correctness.
- Cost: threads queue up waiting for the lock — throughput drops under high contention on a hot product (e.g. a flash sale item).
- DB equivalent: `SELECT ... FOR UPDATE` (row lock) inside a transaction.

**Optimistic concurrency control (OCC)** — don't lock; read a `version` number alongside the value, do the work, then write back *only if the version hasn't changed since you read it*. If it changed, someone else won the race — retry.
```python
def try_decrement(inventory, quantity):
    old_version = inventory.version
    if inventory.stock < quantity:
        return False
    new_stock = inventory.stock - quantity
    # compare-and-swap: only commits if version still matches
    return inventory.compare_and_swap(old_version, new_stock)
```
- DB equivalent: `UPDATE inventory SET stock = stock - qty, version = version + 1 WHERE id = ? AND version = ? AND stock >= qty` — a single atomic statement, no explicit lock held.
- Better throughput when conflicts are rare; worse when conflicts are frequent (constant retries).
- **This `UPDATE ... WHERE stock >= qty` single-statement trick is worth memorizing** — it's the most common real-world answer to "how do you prevent overselling in SQL" and sidesteps needing an explicit lock at all, because the database's own row-level atomicity does the check-and-decrement as one indivisible operation.

**How to decide which to present**: pessimistic (in-process lock) is fine and simpler to code live in an interview. Mention OCC / the SQL `WHERE stock >= qty` pattern as the production-grade answer when asked to go deeper — you don't need to implement OCC from scratch to get credit for knowing it exists and why it's often the better real answer.

---

## 5. Immediate Deduction (chosen), and Reserve/Confirm/Release (considered, not built)

This build deducts stock directly and immediately (`deduct_stock`) rather than holding a claim first — deliberately, to stay simple and tightly matched to the spec in §1, which never asks for cart/checkout-style holds.

**If asked "what about a gap between claiming stock and committing to it"** (e.g. this fed a cart/checkout flow) — that's exactly when immediate deduction becomes wrong, and the standard fix is a **reserve → confirm → release** flow instead: hold `quantity` against a `reservation_id` without deducting yet (`available = total - reserved`), confirm (permanent deduct) once the caller's downstream step succeeds, or release (give the hold back) if it fails/times out. This needs its own `Reservation` entity (`reservation_id`, quantity, `expires_at`, status), and abandoned holds should expire **lazily** — checked on next access (`now > expires_at`), the same trick as Token Bucket's lazy refill — not via a background sweep thread. Good to have ready as a follow-up answer; not part of this build.

---

## 6. Why There's No Order State Machine Here

An earlier pass through this problem explored a full `Order` state machine (`Placed → Reserved → Confirmed → Shipped → Delivered`, with a `Cancelled` branch) inside this system. That's now **explicitly out of scope** (§1) — a deliberate Single-Responsibility call at the system-boundary level, not just the class level: this system's job is "safely track and update stock per store," not "orchestrate a customer's purchase lifecycle." `Order`, cart, checkout, and payment status belong to a separate Order/Checkout service that would *call into* this system's plain create/update/deduct API — not live inside it.

If asked "why doesn't your inventory system handle orders," the answer is this scope cut, stated as a deliberate architectural boundary (mirrors how real systems split an Inventory Service from an Order Service), not an omission.

---

## 7. Distributed Consistency (the "how would this scale" follow-up)

Single-process `threading.Lock()` only works if all requests for a given store/product are handled by *one* process. Once you have multiple app servers behind a load balancer, all hitting a shared database:

- **Strong consistency, simplest to reason about**: push the check-and-decrement into the database itself via the `UPDATE ... WHERE stock >= qty` pattern (§4) — the DB's row-level locking/atomicity does the work, no application-level lock needed at all.
- **Distributed lock** (Redis-based, e.g. Redlock): needed only if the critical section spans *more* than one atomic DB statement (e.g. you need to touch multiple tables/services as one unit). Heavier and more failure-prone than pushing the logic into a single DB statement — prefer the DB approach when possible, mention the distributed lock as the fallback when a single-statement update genuinely isn't enough (e.g. reserving stock across two different microservices).
- **Cache-aside inconsistency risk**: if you're also caching stock counts for fast reads (common in quick-commerce for the product listing page), that cache is allowed to be *eventually* consistent (a slightly stale "12 left" shown to the browsing customer is fine) — but the actual deduction on checkout must always go through the source of truth (DB), never trust the cache for the write path. Good distinction to draw if asked about caching.

---

## 8. Idempotency

A retried `deduct_stock`/`add_stock` call (client timeout + automatic retry, or a flaky network) must not double-deduct or double-add stock. Standard fix: the caller sends an **idempotency key** (a UUID generated once per logical action) with the request; this system checks "have I already processed this key?" before doing any work, and if so, returns the previously-computed result instead of redoing the mutation. Worth a mention even if not implemented — a common interviewer follow-up on any "mutate shared state" flow.

---

## 9. Data Modeling — Why Product and Inventory Are Separate Entities

Earlier problems (Parking Lot, Vending Machine) had one location, so "the thing" and "how many are left" lived together naturally. Here they need to be split:

| Entity | Changes how often | Responsibility |
|---|---|---|
| `Product` | Rarely (catalog data: name, price, category) | Read-heavy, same across all stores |
| `Store` | Rarely | Identity + location |
| `Inventory` | Constantly (mutable stock count) | One row per `(store_id, product_id)` — this is where all the concurrency control lives |

`Order`/`OrderItem` and `Reservation` deliberately dropped from this table — out of scope per §1/§6 and §5 respectively.

---

## 10. Pattern Mapping for This Problem

| Need | Pattern |
|---|---|
| Owning `Inventory`/`Product` records, keyed lookup, explicit create | Manager (Registry-shaped, like Rate Limiter) |
| Notify on low stock (now a required functional feature, §1) | Observer |
| The public entry point tying `ProductCatalog` + `InventoryManager` together | Context |

No Strategy (store selection is out of scope), no State (order lifecycle is out of scope), no Builder/Decorator/Chain of Responsibility/etc. — don't force patterns the problem doesn't call for. This is a notably smaller pattern set than the earlier, broader exploration of this problem used — a sign the scoped-down spec is actually simpler to build correctly, not a sign of missing depth.

---

## 11. How to Frame This Out Loud in the Interview

A rough narrative arc that hits all the high-value points without over-explaining:

1. State the requirements, the explicit out-of-scope list, and the open "centralized vs per-store manager" question from §1 — leading with a deliberate scope cut reads as judgment, not a gap.
2. List entities (§9 table) — explain *why* Product and Inventory are split.
3. Say the concurrency problem out loud before being asked: "the core challenge here is preventing two concurrent updates from overselling the same stock — I'll handle that with either an in-process lock per inventory record, or, if this needs to be production-grade / distributed, a single atomic `UPDATE ... WHERE stock >= qty` at the DB layer."
4. Be ready to explain *why* there's no Order state machine (§6) and no Reservation/hold layer (§5) if asked — both are deliberate scope cuts with a one-line reserve/confirm/release answer ready if pushed on "what about checkout gaps."
5. If asked to go further: idempotency, cache-aside consistency for the read path, distributed locks as the heavier fallback, lock striping given "millions of products" (§12).

This ordering front-loads the part interviewers actually care about (concurrency correctness) instead of burying it at the end.

---

## 12. Two Granularities of Locking: Per-Key Create Lock vs Record-Level Mutation Lock

Concurrency control isn't one lock — it's (at least) two, protecting two different kinds of race. And within the create-side lock, the naive version (one lock for the whole manager) is itself a mistake worth catching before it ships.

**Record-level lock** (§4) — protects mutation of an *existing* `Inventory` (or `Product`) record: `deduct`, `add`, `deactivate`. One lock per record (owned by the record itself), so unrelated products never block each other. This is the hot path (called on every stock update), so granularity matters for throughput.

**Create-path lock** — protects the *creation* of a new record, i.e. the check-then-insert into the Manager's dict (`create_inventory_record`, `create_product`). There's no per-record lock to use yet, because the record doesn't exist until the insert completes — the race is on the dict itself: two threads both check `key not in records` (both see `False`), both proceed to insert, one silently clobbers the other.

**First instinct — one lock for the whole manager — is too coarse.** It would serialize *every* create against every other, even for completely unrelated stores/products (`store_1` onboarding "milk" would block `store_2` onboarding "bread"). The fix: **one lock per key** — `(store_id, product_id)` for `InventoryManager`, `product_id` for `ProductCatalog` — so only a genuine collision on the *same* key ever contends.

**The bootstrapping problem this creates, and its fix.** You can't just do `locks[key] = Lock()` on demand without protection — two threads racing to create the lock for the same new key would each construct a *different* `Lock()` object, and whichever write wins the dict leaves the two threads holding non-equal locks that don't actually exclude each other. Fix: a single small `_bootstrap_lock`, held only for the instant of creating a *new* per-key lock, using **double-checked locking** — check without the lock first (fast path, zero contention once the key's lock exists), only take `_bootstrap_lock` if missing, then check again inside it in case another thread just created it. This is the exact same technique as the thread-safe Singleton pattern (`LLD_INTERVIEW_REVISION.md` §7) — same trick, different use case.

**Concurrency behavior matrix** (identical shape for both the create path and the update path — only which lock object is involved changes):

| Scenario | Result |
|---|---|
| Same store, same product, concurrent | Same lock → serialized correctly (second create gets a clean "already exists" error; second update runs right after the first completes, seeing its result). |
| Same store, different products, concurrent | Different keys → different locks → **fully parallel**, no blocking. |
| Different stores, concurrent (same or different product id) | Key always includes `store_id` → always different locks → **fully parallel**. |

**Common misconception worth heading off**: "Python has the GIL, so this is already safe." The GIL guarantees a single bytecode operation is atomic — it does *not* make a multi-statement sequence like `if key not in d: d[key] = value` atomic as a whole. A thread can be paused by the interpreter right between the check and the insert. The GIL protects individual operations, not compound check-then-act logic spanning multiple statements — which is exactly why the explicit lock (both the per-key lock and the bootstrap lock protecting its creation) is still required.

**Scaling follow-up, if asked**: one `Lock` object per distinct key, kept forever, is unbounded memory if the key space is huge (millions of SKUs × stores). The production answer is **lock striping** (what Java's `ConcurrentHashMap` does): pre-allocate a fixed pool of N locks (e.g. 256) and hash each key into one via `locks[hash(key) % N]`. Trades a small amount of false contention (two unrelated keys occasionally landing on the same stripe) for bounded memory — worth naming, not necessary to build for this exercise.

**How to frame this if asked "how do you handle concurrent writes"**: don't answer with just one lock, and don't stop at "per store." Name the actual shape — "record-level locking for mutating an existing item, and a separate per-key lock (not a single global one) for the create-if-absent race on the collection itself, bootstrapped safely via double-checked locking" — since under-specifying granularity (store-level, or worse, one global lock) is the actual bug this section exists to catch.

---

## Next Step

Once this is comfortable, we move to `design.md` (same shape as the Rate Limiter one): concrete class list, method signatures, and the build order for actually coding it.
