from datetime import datetime, timedelta, timezone

from borderpay.agent.decision import TrendHypothesis
from borderpay.agent.groq_agent import GroqAgent
from borderpay.domain.belief import BeliefState
from borderpay.domain.transfer import TransferTarget
from borderpay.environment.fx_feed import LiveFxFeed


# 1. Fetch live FX rate
feed = LiveFxFeed()
observation = feed.observe()

print()
print("=== Live FX Observation ===")
print("Timestamp:", observation.timestamp.isoformat())
print("USD/INR:", observation.usd_inr_rate)


# 2. Create transfer target
target = TransferTarget(
    target_inr_minor=1_000_000,  # ₹10,000
    deadline=datetime.now(timezone.utc) + timedelta(hours=24),
    usd_budget_minor=150_000,  # $1,500
)


# 3. Create current belief
belief = BeliefState(target=target)
belief.observe_fx(observation)


# 4. Ask Groq to make the timing decision
agent = GroqAgent()

decision = agent.decide(
    belief,
    recent_observations=[observation.usd_inr_rate],
    previous_trend_hypothesis=TrendHypothesis.UNCERTAIN,
    previous_reasoning=(
        "This is the first live observation, so there is not enough "
        "history to establish a reliable trend."
    ),
)


# 5. Display decision
print()
print("=== BorderPay Agent Decision ===")
print("Action:", decision.action.value)
print("Proposed INR:", decision.proposed_inr_minor / 100)
print("Trend:", decision.trend_hypothesis.value)
print("Confidence:", decision.confidence)
print("Reasoning:", decision.reasoning)