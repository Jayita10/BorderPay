from borderpay.guardrails.target import cap_to_target


result = cap_to_target(
    proposed_inr_minor=150_000,
    remaining_inr_minor=100_000,
)

print(f"Proposed: ₹{150_000 / 100:,.2f}")
print(f"Remaining target: ₹{100_000 / 100:,.2f}")
print(f"Approved: ₹{result / 100:,.2f}")

assert result == 100_000

print("Target guardrail: PASS")