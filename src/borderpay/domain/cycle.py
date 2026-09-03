from dataclasses import dataclass
from datetime import datetime

from borderpay.agent.decision import AgentDecision, TrendHypothesis
from borderpay.domain.models import FxObservation


@dataclass(frozen=True)
class CycleRecord:
    cycle_number: int
    timestamp: datetime
    fx_observation: FxObservation
    remaining_inr_minor: int
    remaining_usd_minor: int
    decision: AgentDecision
    previous_trend_hypothesis: TrendHypothesis | None
    previous_reasoning: str | None