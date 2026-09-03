from borderpay.guardrails.engine import evaluate_conversion


result = evaluate_conversion(
    proposed_inr_minor=100_000,
    remaining_inr_minor=100_000,
    remaining_usd_minor=100_000,
    usd_inr_rate=94.48,
)

print(result)

assert result.approved
assert result.approved_inr_minor <= 100_000

print("Combined guardrails: PASS")