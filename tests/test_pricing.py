
"""Unit tests for analytical pricing models."""

import numpy as np
import pytest

from src.pricing.black_scholes import black_scholes_price
from src.pricing.forward import forward_price, forward_value


def test_black_scholes_call():
    price = black_scholes_price(
        spot=100.0,
        strike=100.0,
        maturity=1.0,
        risk_free_rate=0.05,
        volatility=0.20,
        option_type="call",
    )

    assert price == pytest.approx(10.4506, abs=1e-4)


def test_black_scholes_put():
    price = black_scholes_price(
        spot=100.0,
        strike=100.0,
        maturity=1.0,
        risk_free_rate=0.05,
        volatility=0.20,
        option_type="put",
    )

    assert price == pytest.approx(5.5735, abs=1e-4)


def test_put_call_parity():
    call = black_scholes_price(
        100.0, 100.0, 1.0, 0.05, 0.20, "call"
    )

    put = black_scholes_price(
        100.0, 100.0, 1.0, 0.05, 0.20, "put"
    )

    expected_difference = 100.0 - 100.0 * np.exp(-0.05)

    assert call - put == pytest.approx(expected_difference)


def test_forward_price():
    price = forward_price(
        spot=100.0,
        maturity=1.0,
        risk_free_rate=0.05,
    )

    assert price == pytest.approx(105.1271, abs=1e-4)


def test_new_forward_has_zero_initial_value():
    delivery_price = forward_price(
        spot=100.0,
        maturity=1.0,
        risk_free_rate=0.05,
    )

    value = forward_value(
        spot=100.0,
        delivery_price=delivery_price,
        maturity=1.0,
        risk_free_rate=0.05,
    )

    assert value == pytest.approx(0.0, abs=1e-10)


def test_forward_value():
    value = forward_value(
        spot=100.0,
        delivery_price=100.0,
        maturity=1.0,
        risk_free_rate=0.05,
    )

    assert value == pytest.approx(4.8771, abs=1e-4)


def test_invalid_option_type():
    with pytest.raises(ValueError):
        black_scholes_price(
            100.0, 100.0, 1.0, 0.05, 0.20, "invalid"
        )


def test_negative_volatility():
    with pytest.raises(ValueError):
        black_scholes_price(
            100.0, 100.0, 1.0, 0.05, -0.20
        )
