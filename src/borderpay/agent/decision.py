from dataclasses import dataclass
from enum import Enum


class DecisionAction(str, Enum):
    HOLD = "hold"
    CONVERT_PARTIAL = "convert_partial"
    CONVERT_FULL = "convert_full"


class TrendHypothesis(str, Enum):
    IMPROVING = "improving"
    WORSENING = "worsening"
    UNCERTAIN = "uncertain"


@dataclass(frozen=True)
class AgentDecision:
    action: DecisionAction
    proposed_inr_minor: int
    trend_hypothesis: TrendHypothesis
    confidence: float
    reasoning: str

    def __post_init__(self) -> None:
        if self.proposed_inr_minor < 0:
            raise ValueError("proposed_inr_minor must not be negative")

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

        if not self.reasoning.strip():
            raise ValueError("reasoning must not be empty")