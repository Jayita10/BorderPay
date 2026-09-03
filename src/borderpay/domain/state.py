from dataclasses import dataclass, field

from borderpay.agent.decision import TrendHypothesis
from borderpay.domain.belief import BeliefState
from borderpay.domain.cycle import CycleRecord
from borderpay.domain.models import FxObservation


@dataclass
class BorderPayState:
    belief: BeliefState
    observations: list[FxObservation] = field(default_factory=list)
    cycles: list[CycleRecord] = field(default_factory=list)

    @property
    def cycle_number(self) -> int:
        return len(self.cycles) + 1

    @property
    def previous_trend_hypothesis(self) -> TrendHypothesis | None:
        if not self.cycles:
            return None

        return self.cycles[-1].decision.trend_hypothesis

    @property
    def previous_reasoning(self) -> str | None:
        if not self.cycles:
            return None

        return self.cycles[-1].decision.reasoning

    def record_observation(self, observation: FxObservation) -> None:
        self.observations.append(observation)
        self.belief.observe_fx(observation)

    def record_cycle(self, record: CycleRecord) -> None:
        self.cycles.append(record)