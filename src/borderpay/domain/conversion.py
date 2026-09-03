from dataclasses import dataclass
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR


@dataclass(frozen=True)
class ConversionQuote:
    requested_inr_minor: int
    fixed_fee_inr_minor: int
    proportional_fee_minor: int
    total_inr_minor: int
    usd_required_minor: int


def quote_conversion(
    *,
    requested_inr_minor: int,
    usd_inr_rate: float,
    proportional_fee_bps: int = 150,
    fixed_fee_inr_minor: int = 4_000,
) -> ConversionQuote:
    if requested_inr_minor <= 0:
        raise ValueError("requested_inr_minor must be positive")

    if usd_inr_rate <= 0:
        raise ValueError("usd_inr_rate must be positive")

    if proportional_fee_bps < 0:
        raise ValueError("proportional_fee_bps must not be negative")

    if fixed_fee_inr_minor < 0:
        raise ValueError("fixed_fee_inr_minor must not be negative")

    amount_with_fixed_fee = (
        requested_inr_minor + fixed_fee_inr_minor
    )

    proportional_fee = (
        Decimal(amount_with_fixed_fee)
        * Decimal(proportional_fee_bps)
        / Decimal(10_000)
    ).quantize(
        Decimal("1"),
        rounding=ROUND_FLOOR,
    )

    proportional_fee_minor = int(proportional_fee)

    total_inr_minor = (
        amount_with_fixed_fee
        + proportional_fee_minor
    )

    usd_required = (
        Decimal(total_inr_minor)
        / Decimal(str(usd_inr_rate))
    )

    usd_required_minor = int(
        usd_required.quantize(
            Decimal("1"),
            rounding=ROUND_CEILING,
        )
    )

    return ConversionQuote(
        requested_inr_minor=requested_inr_minor,
        fixed_fee_inr_minor=fixed_fee_inr_minor,
        proportional_fee_minor=proportional_fee_minor,
        total_inr_minor=total_inr_minor,
        usd_required_minor=usd_required_minor,
    )