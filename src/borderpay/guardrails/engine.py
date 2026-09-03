from dataclasses import dataclass

from borderpay.domain.conversion import quote_conversion
from borderpay.guardrails.budget import max_affordable_inr_minor
from borderpay.guardrails.target import cap_to_target


@dataclass(frozen=True)
class GuardrailResult:
    approved: bool
    approved_inr_minor: int
    reason: str
    budget_limited: bool
    target_limited: bool


def evaluate_conversion(
    *,
    proposed_inr_minor: int,
    remaining_inr_minor: int,
    remaining_usd_minor: int,
    usd_inr_rate: float,
    proportional_fee_bps: int = 150,
    fixed_fee_inr_minor: int = 4_000,
) -> GuardrailResult:

    if proposed_inr_minor < 0:
        raise ValueError("proposed_inr_minor must not be negative")

    if remaining_inr_minor < 0:
        raise ValueError("remaining_inr_minor must not be negative")

    if remaining_usd_minor < 0:
        raise ValueError("remaining_usd_minor must not be negative")

    if remaining_inr_minor == 0:
        return GuardrailResult(
            approved=False,
            approved_inr_minor=0,
            reason="transfer target already met",
            budget_limited=False,
            target_limited=False,
        )

    affordable = max_affordable_inr_minor(
        remaining_usd_minor=remaining_usd_minor,
        usd_inr_rate=usd_inr_rate,
        proportional_fee_bps=proportional_fee_bps,
        fixed_fee_inr_minor=fixed_fee_inr_minor,
    )

    target_capped = cap_to_target(
        proposed_inr_minor=proposed_inr_minor,
        remaining_inr_minor=remaining_inr_minor,
    )

    approved_amount = min(
        target_capped,
        affordable,
    )

    if approved_amount == 0:
        return GuardrailResult(
            approved=False,
            approved_inr_minor=0,
            reason="conversion is not affordable within remaining budget",
            budget_limited=True,
            target_limited=target_capped < proposed_inr_minor,
        )

    budget_limited = affordable < target_capped
    target_limited = remaining_inr_minor < proposed_inr_minor

    reasons = []

    if budget_limited:
        reasons.append("limited by remaining USD budget")

    if target_limited:
        reasons.append("limited by remaining INR target")

    if not reasons:
        reasons.append("conversion satisfies all guardrails")

    return GuardrailResult(
        approved=True,
        approved_inr_minor=approved_amount,
        reason="; ".join(reasons),
        budget_limited=budget_limited,
        target_limited=target_limited,
    )