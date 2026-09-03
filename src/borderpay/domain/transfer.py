from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TransferTarget:
    target_inr_minor: int
    deadline: datetime
    usd_budget_minor: int

    def __post_init__(self) -> None:
        if self.target_inr_minor <= 0:
            raise ValueError("target_inr_minor must be positive")

        if self.usd_budget_minor <= 0:
            raise ValueError("usd_budget_minor must be positive")

    @property
    def target_inr(self) -> float:
        return self.target_inr_minor / 100

    @property
    def usd_budget(self) -> float:
        return self.usd_budget_minor / 100