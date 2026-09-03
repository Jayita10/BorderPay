from datetime import datetime, timedelta, timezone

from borderpay.agent.decision import AgentDecision, DecisionAction, TrendHypothesis
from borderpay.domain.belief import BeliefState
from borderpay.domain.cycle import CycleRecord
from borderpay.domain.models import FxObservation
from borderpay.domain.state import BorderPayState
from borderpay.domain.transfer import TransferTarget


target = TransferTarget(
    target_inr_minor=1_000_000,
    deadline=datetime.now(timezone.utc) + timedelta(hours=24),
    usd_budget_minor=150_000,
)

belief = BeliefState(target=target)
state = BorderPayState(belief=belief)


# Cycle 1 observation
observation_1 = FxObservation(
    timestamp=datetime.now(timezone.utc),
    usd_inr_rate=94.47,
)

state.record_observation(observation_1)

decision_1 = AgentDecision(
    action=DecisionAction.HOLD,
    proposed_inr_minor=0,
    trend_hypothesis=TrendHypothesis.UNCERTAIN,
    confidence=0.5,
    reasoning="There is not enough history to establish a reliable trend.",
)

record_1 = CycleRecord(
    cycle_number=state.cycle_number,
    timestamp=observation_1.timestamp,
    fx_observation=observation_1,
    remaining_inr_minor=state.belief.remaining_inr_minor,
    remaining_usd_minor=state.belief.remaining_usd_minor,
    decision=decision_1,
    previous_trend_hypothesis=state.previous_trend_hypothesis,
    previous_reasoning=state.previous_reasoning,
)

state.record_cycle(record_1)


# Cycle 2 observation
observation_2 = FxObservation(
    timestamp=datetime.now(timezone.utc),
    usd_inr_rate=94.70,
)

state.record_observation(observation_2)

decision_2 = AgentDecision(
    action=DecisionAction.HOLD,
    proposed_inr_minor=0,
    trend_hypothesis=TrendHypothesis.IMPROVING,
    confidence=0.65,
    reasoning="The rate has improved, but more observations are needed.",
)

record_2 = CycleRecord(
    cycle_number=state.cycle_number,
    timestamp=observation_2.timestamp,
    fx_observation=observation_2,
    remaining_inr_minor=state.belief.remaining_inr_minor,
    remaining_usd_minor=state.belief.remaining_usd_minor,
    decision=decision_2,
    previous_trend_hypothesis=state.previous_trend_hypothesis,
    previous_reasoning=state.previous_reasoning,
)

state.record_cycle(record_2)


print("=== BorderPay Cycle State ===")
print("Total observations:", len(state.observations))
print("Total cycles:", len(state.cycles))
print("Latest rate:", state.belief.latest_fx.usd_inr_rate)
print("Previous trend:", state.previous_trend_hypothesis.value)
print("Previous reasoning:", state.previous_reasoning)