from dataclasses import dataclass

from borderpay.domain.models import FxObservation
from borderpay.domain.transfer import TransferTarget


@dataclass
class BeliefState:
    target: TransferTarget
    secured_inr_minor: int = 0
    usd_spent_minor: int = 0
    latest_fx: FxObservation | None = None

    def __post_init__(self) -> None:
        if self.secured_inr_minor < 0:
            raise ValueError("secured_inr_minor must not be negative")

        if self.usd_spent_minor < 0:
            raise ValueError("usd_spent_minor must not be negative")

    @property
    def remaining_inr_minor(self) -> int:
        return max(
            0,
            self.target.target_inr_minor - self.secured_inr_minor,
        )

    @property
    def remaining_usd_minor(self) -> int:
        return max(
            0,
            self.target.usd_budget_minor - self.usd_spent_minor,
        )

    @property
    def is_target_met(self) -> bool:
        return self.remaining_inr_minor == 0

    @property
    def budget_exhausted(self) -> bool:
        return self.remaining_usd_minor == 0

    def observe_fx(self, observation: FxObservation) -> None:
        self.latest_fx = observation