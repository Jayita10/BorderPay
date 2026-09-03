from borderpay.domain.conversion import quote_conversion


def max_affordable_inr_minor(
    *,
    remaining_usd_minor: int,
    usd_inr_rate: float,
    proportional_fee_bps: int = 150,
    fixed_fee_inr_minor: int = 4_000,
) -> int:
    if remaining_usd_minor < 0:
        raise ValueError("remaining_usd_minor must not be negative")

    if usd_inr_rate <= 0:
        raise ValueError("usd_inr_rate must be positive")

    if remaining_usd_minor == 0:
        return 0

    low = 0
    high = int(
        remaining_usd_minor
        * usd_inr_rate
    )

    best = 0

    while low <= high:
        middle = (low + high) // 2

        if middle == 0:
            low = 1
            continue

        quote = quote_conversion(
            requested_inr_minor=middle,
            usd_inr_rate=usd_inr_rate,
            proportional_fee_bps=proportional_fee_bps,
            fixed_fee_inr_minor=fixed_fee_inr_minor,
        )

        if quote.usd_required_minor <= remaining_usd_minor:
            best = middle
            low = middle + 1
        else:
            high = middle - 1

    return best