import os
from datetime import datetime, timezone
from random import Random

import httpx
from dotenv import load_dotenv

from borderpay.domain.models import FxObservation


load_dotenv()


class SimulatedFxFeed:
    def __init__(
        self,
        initial_rate: float = 84.0,
        volatility: float = 0.35,
        seed: int = 42,
    ) -> None:
        if initial_rate <= 0:
            raise ValueError("initial_rate must be positive")

        if volatility < 0:
            raise ValueError("volatility must not be negative")

        self.rate = initial_rate
        self.volatility = volatility
        self.random = Random(seed)

    def observe(self) -> FxObservation:
        movement = self.random.uniform(
            -self.volatility,
            self.volatility,
        )

        self.rate = max(0.01, self.rate + movement)

        return FxObservation(
            timestamp=datetime.now(timezone.utc),
            usd_inr_rate=round(self.rate, 4),
        )


class LiveFxFeed:
    API_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")

        if not self.api_key:
            raise ValueError(
                "ALPHA_VANTAGE_API_KEY is not configured"
            )

    def observe(self) -> FxObservation:
        params = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": "USD",
            "to_currency": "INR",
            "apikey": self.api_key,
        }

        response = httpx.get(
            self.API_URL,
            params=params,
            timeout=5.0,
        )

        response.raise_for_status()

        data = response.json()

        if "Realtime Currency Exchange Rate" not in data:
            raise ValueError(
                f"Alpha Vantage returned unexpected data: {data}"
            )

        rate_data = data["Realtime Currency Exchange Rate"]

        rate = float(
            rate_data["5. Exchange Rate"]
        )

        if rate <= 0:
            raise ValueError(
                "Alpha Vantage returned invalid USD/INR rate"
            )

        return FxObservation(
            timestamp=datetime.now(timezone.utc),
            usd_inr_rate=rate,
        )