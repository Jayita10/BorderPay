from datetime import datetime


def deadline_has_passed(
    *,
    now: datetime,
    deadline: datetime,
) -> bool:
    return now >= deadline


def required_rate_for_remaining_target(
    *,
    remaining_inr_minor: int,
    remaining_usd_minor: int,
) -> float | None:
    if remaining_inr_minor < 0:
        raise ValueError("remaining_inr_minor must not be negative")

    if remaining_usd_minor <= 0:
        return None

    if remaining_inr_minor == 0:
        return 0.0

    return remaining_inr_minor / remaining_usd_minor