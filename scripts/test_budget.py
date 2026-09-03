from borderpay.domain.conversion import quote_conversion
from borderpay.guardrails.budget import max_affordable_inr_minor


remaining_usd = 1_000_00
rate = 94.48

maximum = max_affordable_inr_minor(
    remaining_usd_minor=remaining_usd,
    usd_inr_rate=rate,
)

quote = quote_conversion(
    requested_inr_minor=maximum,
    usd_inr_rate=rate,
)

print(f"Remaining USD: ${remaining_usd / 100:,.2f}")
print(f"Maximum INR: ₹{maximum / 100:,.2f}")
print(f"USD required: ${quote.usd_required_minor / 100:,.2f}")

assert quote.usd_required_minor <= remaining_usd

next_quote = quote_conversion(
    requested_inr_minor=maximum + 1,
    usd_inr_rate=rate,
)

assert next_quote.usd_required_minor > remaining_usd

print("Budget guardrail: PASS")