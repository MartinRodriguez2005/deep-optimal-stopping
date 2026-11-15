
"""Simulation of correlated multidimensional Geometric Brownian Motions."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def simulate_gbm(
    initial_prices: FloatArray,
    drift: FloatArray,
    volatility: FloatArray,
    correlation: FloatArray,
    maturity: float,
    n_steps: int,
    n_paths: int,
    seed: int | None = None,
) -> FloatArray:
    """Simulate correlated multidimensional GBM paths.

    Args:
        initial_prices: Initial asset prices, shape (n_assets,).
        drift: Annualized drift rates, shape (n_assets,).
        volatility: Annualized volatilities, shape (n_assets,).
        correlation: Correlation matrix, shape (n_assets, n_assets).
        maturity: Simulation horizon in years.
        n_steps: Number of time steps.
        n_paths: Number of simulated paths.
        seed: Random seed for reproducibility.

    Returns:
        Simulated paths of shape (n_paths, n_steps + 1, n_assets).
    """
    initial_prices = np.asarray(initial_prices, dtype=np.float64)
    drift = np.asarray(drift, dtype=np.float64)
    volatility = np.asarray(volatility, dtype=np.float64)
    correlation = np.asarray(correlation, dtype=np.float64)

    if initial_prices.ndim != 1 or initial_prices.size == 0:
        raise ValueError("initial_prices must be a non-empty 1D array")

    n_assets = initial_prices.size

    if drift.shape != (n_assets,):
        raise ValueError("drift must have one value per asset")

    if volatility.shape != (n_assets,):
        raise ValueError("volatility must have one value per asset")

    if correlation.shape != (n_assets, n_assets):
        raise ValueError("correlation has an invalid shape")

    if not all(
        np.all(np.isfinite(array))
        for array in (initial_prices, drift, volatility, correlation)
    ):
        raise ValueError("All input arrays must contain finite values")

    if np.any(initial_prices <= 0):
        raise ValueError("Initial prices must be positive")

    if np.any(volatility < 0):
        raise ValueError("Volatility cannot be negative")

    if maturity <= 0 or n_steps <= 0 or n_paths <= 0:
        raise ValueError("maturity, n_steps and n_paths must be positive")

    if not np.allclose(correlation, correlation.T):
        raise ValueError("Correlation matrix must be symmetric")

    if not np.allclose(np.diag(correlation), 1.0):
        raise ValueError("Correlation diagonal must equal one")

    try:
        cholesky = np.linalg.cholesky(correlation)
    except np.linalg.LinAlgError as exc:
        raise ValueError(
            "Correlation matrix must be positive definite"
        ) from exc

    rng = np.random.default_rng(seed)

    dt = maturity / n_steps

    independent_normals = rng.standard_normal(
        size=(n_paths, n_steps, n_assets)
    )

    correlated_normals = independent_normals @ cholesky.T

    increments = (
        (drift - 0.5 * volatility**2) * dt
        + volatility * np.sqrt(dt) * correlated_normals
    )

    log_returns = np.cumsum(increments, axis=1)

    paths = np.empty(
        (n_paths, n_steps + 1, n_assets),
        dtype=np.float64,
    )

    paths[:, 0, :] = initial_prices

    paths[:, 1:, :] = (
        initial_prices[None, None, :] * np.exp(log_returns)
    )

    return paths

