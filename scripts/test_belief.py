from datetime import datetime, timedelta, timezone

from borderpay.domain.belief import BeliefState
from borderpay.domain.models import FxObservation
from borderpay.domain.transfer import TransferTarget


target = TransferTarget(
    target_inr_minor=1_000_000,
    deadline=datetime.now(timezone.utc) + timedelta(hours=24),
    usd_budget_minor=1_500_00,
)

belief = BeliefState(target=target)

print(f"Target: ₹{belief.target.target_inr:,.2f}")
print(f"Secured: ₹{belief.secured_inr_minor / 100:,.2f}")
print(f"Remaining: ₹{belief.remaining_inr_minor / 100:,.2f}")
print(f"USD remaining: ${belief.remaining_usd_minor / 100:,.2f}")

observation = FxObservation(
    timestamp=datetime.now(timezone.utc),
    usd_inr_rate=94.48,
)

belief.observe_fx(observation)

print(f"Latest USD/INR: ₹{belief.latest_fx.usd_inr_rate}")