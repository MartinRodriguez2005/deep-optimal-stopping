
"""Unit tests for the GBM simulation module."""

import numpy as np
import pytest

from src.simulation.gbm import simulate_gbm


@pytest.fixture
def simulation_parameters():
    return {
        "initial_prices": np.array([100.0, 120.0]),
        "drift": np.array([0.05, 0.03]),
        "volatility": np.array([0.20, 0.25]),
        "correlation": np.array([
            [1.0, 0.5],
            [0.5, 1.0],
        ]),
        "maturity": 1.0,
        "n_steps": 252,
        "n_paths": 1000,
        "seed": 42,
    }


def test_output_shape(simulation_parameters):
    paths = simulate_gbm(**simulation_parameters)

    assert paths.shape == (1000, 253, 2)


def test_initial_prices_are_preserved(simulation_parameters):
    paths = simulate_gbm(**simulation_parameters)

    expected = np.tile(
        simulation_parameters["initial_prices"],
        (1000, 1),
    )

    np.testing.assert_allclose(paths[:, 0, :], expected)


def test_prices_are_positive(simulation_parameters):
    paths = simulate_gbm(**simulation_parameters)

    assert np.all(paths > 0)


def test_reproducibility(simulation_parameters):
    first = simulate_gbm(**simulation_parameters)
    second = simulate_gbm(**simulation_parameters)

    np.testing.assert_array_equal(first, second)


def test_invalid_correlation_matrix(simulation_parameters):
    parameters = simulation_parameters.copy()

    parameters["correlation"] = np.array([
        [1.0, 1.5],
        [1.5, 1.0],
    ])

    with pytest.raises(ValueError):
        simulate_gbm(**parameters)

def test_terminal_mean_matches_theory():
    n_paths = 100_000

    s0 = 100.0
    mu = 0.05
    sigma = 0.20
    maturity = 1.0

    paths = simulate_gbm(
        initial_prices=np.array([s0]),
        drift=np.array([mu]),
        volatility=np.array([sigma]),
        correlation=np.array([[1.0]]),
        maturity=maturity,
        n_steps=252,
        n_paths=n_paths,
        seed=42,
    )

    terminal_prices = paths[:, -1, 0]

    theoretical_mean = s0 * np.exp(mu * maturity)

    theoretical_variance = (
        s0**2
        * np.exp(2 * mu * maturity)
        * (np.exp(sigma**2 * maturity) - 1)
    )

    standard_error = np.sqrt(theoretical_variance / n_paths)

    assert abs(
        np.mean(terminal_prices) - theoretical_mean
    ) < 4 * standard_error


def test_terminal_variance_matches_theory():
    n_paths = 100_000

    s0 = 100.0
    mu = 0.05
    sigma = 0.20
    maturity = 1.0

    paths = simulate_gbm(
        initial_prices=np.array([s0]),
        drift=np.array([mu]),
        volatility=np.array([sigma]),
        correlation=np.array([[1.0]]),
        maturity=maturity,
        n_steps=252,
        n_paths=n_paths,
        seed=42,
    )

    terminal_prices = paths[:, -1, 0]

    theoretical_variance = (
        s0**2
        * np.exp(2 * mu * maturity)
        * (np.exp(sigma**2 * maturity) - 1)
    )

    empirical_variance = np.var(terminal_prices, ddof=1)

    assert np.isclose(
        empirical_variance,
        theoretical_variance,
        rtol=0.04,
    )


def test_empirical_correlation():
    n_paths = 50_000

    target_correlation = 0.6

    paths = simulate_gbm(
        initial_prices=np.array([100.0, 100.0]),
        drift=np.array([0.05, 0.05]),
        volatility=np.array([0.20, 0.20]),
        correlation=np.array([
            [1.0, target_correlation],
            [target_correlation, 1.0],
        ]),
        maturity=1.0,
        n_steps=252,
        n_paths=n_paths,
        seed=42,
    )

    terminal_log_returns = np.log(
        paths[:, -1, :] / paths[:, 0, :]
    )

    empirical_correlation = np.corrcoef(
        terminal_log_returns.T
    )[0, 1]

    assert abs(
        empirical_correlation - target_correlation
    ) < 0.015
