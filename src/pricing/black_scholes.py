
"""Analytical Black-Scholes pricing for European options."""

from typing import Literal

import numpy as np
from scipy.stats import norm

OptionType = Literal["call", "put"]


def black_scholes_price(
    spot: float,
    strike: float,
    maturity: float,
    risk_free_rate: float,
    volatility: float,
    option_type: OptionType = "call",
    dividend_yield: float = 0.0,
) -> float:
    """Calculate the Black-Scholes price of a European option.

    Rates and volatility are continuously compounded / annualized.
    """
    parameters = (
        spot,
        strike,
        maturity,
        risk_free_rate,
        volatility,
        dividend_yield,
    )

    if not all(np.isfinite(x) for x in parameters):
        raise ValueError("All parameters must be finite")

    if spot <= 0 or strike <= 0:
        raise ValueError("Spot and strike must be positive")

    if maturity < 0 or volatility < 0:
        raise ValueError("Maturity and volatility cannot be negative")

    if option_type not in ("call", "put"):
        raise ValueError("option_type must be 'call' or 'put'")

    # At maturity, the option is worth its intrinsic value.
    if maturity == 0:
        return (
            max(spot - strike, 0.0)
            if option_type == "call"
            else max(strike - spot, 0.0)
        )

    discounted_spot = spot * np.exp(-dividend_yield * maturity)
    discounted_strike = strike * np.exp(-risk_free_rate * maturity)

    # Deterministic limit when volatility is zero.
    if volatility == 0:
        if option_type == "call":
            return max(discounted_spot - discounted_strike, 0.0)
        return max(discounted_strike - discounted_spot, 0.0)

    d1 = (
        np.log(spot / strike)
        + (
            risk_free_rate
            - dividend_yield
            + 0.5 * volatility**2
        ) * maturity
    ) / (volatility * np.sqrt(maturity))

    d2 = d1 - volatility * np.sqrt(maturity)

    if option_type == "call":
        price = (
            discounted_spot * norm.cdf(d1)
            - discounted_strike * norm.cdf(d2)
        )
    else:
        price = (
            discounted_strike * norm.cdf(-d2)
            - discounted_spot * norm.cdf(-d1)
        )

    return float(price)
