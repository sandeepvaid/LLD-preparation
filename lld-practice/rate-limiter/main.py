from RateLimiter import RateLimiter
from manager.RateLimiterRegistry import RateLimiterRegistry
from strategy.TokenBucketLimiter import TokenBucketLimiter


def main():
    registry = RateLimiterRegistry(strategy_factory=lambda: TokenBucketLimiter(capacity=3, refill_rate=1))
    rate_limiter = RateLimiter(registry)

    print("--- user_1 bursts 5 requests instantly (capacity=3) ---")
    for i in range(5):
        print(f"request {i + 1}: {rate_limiter.allow_request('user_1')}")

    print("\n--- user_2 has its own independent bucket ---")
    print(f"user_2 request 1: {rate_limiter.allow_request('user_2')}")


if __name__ == "__main__":
    main()
