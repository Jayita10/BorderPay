from borderpay.domain.conversion import quote_conversion


quote = quote_conversion(
    requested_inr_minor=100_000,
    usd_inr_rate=94.48,
)

print(f"Requested INR: ₹{quote.requested_inr_minor / 100:,.2f}")
print(f"Fixed fee: ₹{quote.fixed_fee_inr_minor / 100:,.2f}")
print(f"Proportional fee: ₹{quote.proportional_fee_minor / 100:,.2f}")
print(f"Total INR: ₹{quote.total_inr_minor / 100:,.2f}")
print(f"USD required: ${quote.usd_required_minor / 100:,.2f}")