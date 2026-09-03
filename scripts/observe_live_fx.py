from borderpay.environment.fx_feed import LiveFxFeed


feed = LiveFxFeed()

observation = feed.observe()

print(
    f"{observation.timestamp.isoformat()} "
    f"USD/INR = ₹{observation.usd_inr_rate}"
)