from datetime import datetime, timedelta, timezone

from borderpay.domain.transfer import TransferTarget


target = TransferTarget(
    target_inr_minor=100_000_00,
    deadline=datetime.now(timezone.utc) + timedelta(hours=24),
    usd_budget_minor=1_500_00,
)

print(f"Target: ₹{target.target_inr:,.2f}")
print(f"USD budget: ${target.usd_budget:,.2f}")
print(f"Deadline: {target.deadline.isoformat()}")