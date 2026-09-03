from datetime import datetime, timedelta, timezone

from borderpay.guardrails.engine import evaluate_conversion


now = datetime.now(timezone.utc)


print("=== Case 1: Normal conversion ===")

result = evaluate_conversion(
    proposed_inr_minor=500_000,
    remaining_inr_minor=1_000_000,
    remaining_usd_minor=150_000,
    usd_inr_rate=94.48,
    now=now,
    deadline=now + timedelta(hours=24),
)

print(result)


print()
print("=== Case 2: Deadline passed ===")

result = evaluate_conversion(
    proposed_inr_minor=500_000,
    remaining_inr_minor=1_000_000,
    remaining_usd_minor=150_000,
    usd_inr_rate=94.48,
    now=now,
    deadline=now - timedelta(minutes=1),
)

print(result)


print()
print("=== Case 3: Target capped ===")

result = evaluate_conversion(
    proposed_inr_minor=2_000_000,
    remaining_inr_minor=1_000_000,
    remaining_usd_minor=150_000,
    usd_inr_rate=94.48,
    now=now,
    deadline=now + timedelta(hours=24),
)

print(result)


print()
print("=== Case 4: Budget limited ===")

result = evaluate_conversion(
    proposed_inr_minor=1_000_000,
    remaining_inr_minor=1_000_000,
    remaining_usd_minor=10_000,
    usd_inr_rate=94.48,
    now=now,
    deadline=now + timedelta(hours=24),
)

print(result)