
"""Forward contract pricing under continuous compounding."""

import numpy as np


def forward_price(
    spot: float,
    maturity: float,
    risk_free_rate: float,
    dividend_yield: float = 0.0,
) -> float:
    """Calculate the fair forward delivery price at time zero."""
    parameters = (spot, maturity, risk_free_rate, dividend_yield)

    if not all(np.isfinite(x) for x in parameters):
        raise ValueError("All parameters must be finite")

    if spot <= 0:
        raise ValueError("Spot must be positive")

    if maturity < 0:
        raise ValueError("Maturity cannot be negative")

    return float(
        spot * np.exp((risk_free_rate - dividend_yield) * maturity)
    )


def forward_value(
    spot: float,
    delivery_price: float,
    maturity: float,
    risk_free_rate: float,
    dividend_yield: float = 0.0,
) -> float:
    """Calculate the current value of an existing forward contract."""
    parameters = (
        spot,
        delivery_price,
        maturity,
        risk_free_rate,
        dividend_yield,
    )

    if not all(np.isfinite(x) for x in parameters):
        raise ValueError("All parameters must be finite")

    if spot <= 0:
        raise ValueError("Spot must be positive")

    if maturity < 0:
        raise ValueError("Maturity cannot be negative")

    return float(
        spot * np.exp(-dividend_yield * maturity)
        - delivery_price * np.exp(-risk_free_rate * maturity)
    )
