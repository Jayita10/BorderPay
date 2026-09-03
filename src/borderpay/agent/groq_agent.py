import json
import os

from dotenv import load_dotenv
from groq import Groq

from borderpay.agent.decision import (
    AgentDecision,
    DecisionAction,
    TrendHypothesis,
)
from borderpay.domain.belief import BeliefState


load_dotenv()


SYSTEM_PROMPT = """
You are the reasoning layer of BorderPay, a cross-border remittance timing
agent.

A user needs a FIXED net amount of INR to arrive with their recipient by a
deadline. Your job each cycle is to decide whether to hold, partially
convert, or fully convert USD to INR right now.

You do NOT decide safety limits. A separate deterministic guardrail layer
enforces the deadline, target, budget, and conversion constraints regardless
of what you propose.

Your job is the genuinely ambiguous part:
given the FX trend evidence so far, is this a good moment to lock in
progress, or is it better to wait?

You may be wrong. If a new observation contradicts your previous trend
hypothesis, explicitly acknowledge the change and revise the hypothesis.
Changing your mind when the evidence changes is expected behavior.

For USD → INR:
a higher USD/INR rate means more INR can be obtained per USD.

Consider:
- current USD/INR rate
- recent rate observations
- remaining INR target
- remaining USD budget
- time remaining until the deadline
- previous trend hypothesis
- previous reasoning

Do not invent market data or assume future rates.

You are recommending timing only.
You never execute a conversion.

The proposed INR amount is the amount you recommend securing NOW.
It is not a safety authorization. Deterministic guardrails will validate
and potentially reduce it before execution.

Your reasoning must be one or two concise sentences in plain language
because it may be shown directly to the user.
"""


class GroqAgent:
    MODEL = "openai/gpt-oss-120b"

    def __init__(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is not configured")

        self.client = Groq(api_key=api_key)

    def decide(
        self,
        belief: BeliefState,
        recent_observations: list[float] | None = None,
        previous_trend_hypothesis: TrendHypothesis | None = None,
        previous_reasoning: str | None = None,
    ) -> AgentDecision:

        if belief.latest_fx is None:
            return AgentDecision(
                action=DecisionAction.HOLD,
                proposed_inr_minor=0,
                trend_hypothesis=TrendHypothesis.UNCERTAIN,
                confidence=1.0,
                reasoning="There is no current FX observation, so waiting is safer.",
            )

        seconds_remaining = (
            belief.target.deadline - belief.latest_fx.timestamp
        ).total_seconds()

        hours_remaining = max(0.0, seconds_remaining / 3600)

        observations = recent_observations or [
            belief.latest_fx.usd_inr_rate
        ]

        previous_trend = (
            previous_trend_hypothesis.value
            if previous_trend_hypothesis
            else "none"
        )

        previous_reasoning_text = (
            previous_reasoning
            if previous_reasoning
            else "none"
        )

        user_prompt = f"""
Current BorderPay state:

Current USD/INR rate:
{belief.latest_fx.usd_inr_rate}

Recent USD/INR observations:
{observations}

Remaining INR target:
{belief.remaining_inr_minor} minor units

Remaining USD budget:
{belief.remaining_usd_minor} minor units

Time remaining until deadline:
{hours_remaining:.2f} hours

Previous trend hypothesis:
{previous_trend}

Previous reasoning:
{previous_reasoning_text}

Decide whether to hold, partially convert, or fully convert now.

If converting, state the INR amount you recommend securing now.
If holding, the INR amount must be 0.

Base the recommendation only on the evidence available.
Do not invent a trend that the observations do not support.
"""

        response = self.client.chat.completions.create(
            model=self.MODEL,
            reasoning_effort="medium",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "borderpay_agent_decision",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "enum": [
                                    "hold",
                                    "convert_partial",
                                    "convert_full",
                                ],
                            },
                            "inr_amount_to_close": {
                                "type": "integer",
                            },
                            "new_trend_hypothesis": {
                                "type": "string",
                                "enum": [
                                    "improving",
                                    "worsening",
                                    "uncertain",
                                ],
                            },
                            "confidence": {
                                "type": "number",
                            },
                            "reasoning_text": {
                                "type": "string",
                            },
                        },
                        "required": [
                            "action",
                            "inr_amount_to_close",
                            "new_trend_hypothesis",
                            "confidence",
                            "reasoning_text",
                        ],
                        "additionalProperties": False,
                    },
                },
            },
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("Groq returned an empty response")

        data = json.loads(content)

        action = DecisionAction(data["action"])
        proposed_amount = data["inr_amount_to_close"]

        if action == DecisionAction.HOLD:
            proposed_amount = 0

        return AgentDecision(
            action=action,
            proposed_inr_minor=proposed_amount,
            trend_hypothesis=TrendHypothesis(
                data["new_trend_hypothesis"]
            ),
            confidence=data["confidence"],
            reasoning=data["reasoning_text"],
        )