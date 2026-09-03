from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class FxObservation:
    timestamp: datetime
    usd_inr_rate: float

    def __post_init__(self) -> None:
        if self.usd_inr_rate <= 0:
            raise ValueError("USD/INR rate must be positive")