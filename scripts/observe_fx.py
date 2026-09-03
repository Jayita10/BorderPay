from borderpay.environment.fx_feed import SimulatedFxFeed


feed = SimulatedFxFeed()

for _ in range(5):
    observation = feed.observe()

    print(
        f"{observation.timestamp.isoformat()} "
        f"USD/INR = ₹{observation.usd_inr_rate}"
    )