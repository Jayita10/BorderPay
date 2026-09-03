def cap_to_target(
    *,
    proposed_inr_minor: int,
    remaining_inr_minor: int,
) -> int:
    if proposed_inr_minor < 0:
        raise ValueError(
            "proposed_inr_minor must not be negative"
        )

    if remaining_inr_minor < 0:
        raise ValueError(
            "remaining_inr_minor must not be negative"
        )

    return min(
        proposed_inr_minor,
        remaining_inr_minor,
    )