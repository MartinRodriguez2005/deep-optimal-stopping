
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from src.simulation.gbm import simulate_gbm


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="GBM Simulation",
    page_icon="📈",
    layout="wide",
)

st.title("Geometric Brownian Motion")
st.caption("Monte Carlo simulation of stochastic asset price trajectories")


# --------------------------------------------------
# MATHEMATICAL FRAMEWORK
# --------------------------------------------------

with st.expander("Mathematical framework", expanded=True):

    st.subheader("Geometric Brownian Motion")

    st.markdown(
        "Each asset price follows a Geometric Brownian Motion (GBM):"
    )

    st.latex(
        r"dS_t = \mu S_t\,dt + \sigma S_t\,dW_t"
    )

    st.markdown(
        """
        Where:
        - **S(t)**: asset price at time t.
        - **μ**: annualized drift.
        - **σ**: annualized volatility.
        - **W(t)**: standard Brownian motion.
        """
    )

    st.subheader("Exact discrete-time solution")

    st.markdown(
        "The exact solution over a time interval Δt is:"
    )

    st.latex(
        r"S_{t+\Delta t}=S_t\exp\left("
        r"\left(\mu-\frac{\sigma^2}{2}\right)\Delta t"
        r"+\sigma\sqrt{\Delta t}\,Z\right)"
    )

    st.markdown(
        "Where Z follows a standard normal distribution:"
    )

    st.latex(r"Z\sim\mathcal{N}(0,1)")

    st.subheader("Simulation output")

    st.markdown(
        "The simulator returns an array containing all simulated paths:"
    )

    st.latex(
        r"\text{paths}\in\mathbb{R}^{N\times(M+1)\times d}"
    )

    st.markdown(
        """
        - **N**: number of simulated paths.
        - **M + 1**: number of observation dates.
        - **d**: number of assets.
        """
    )


# --------------------------------------------------
# SIDEBAR: SIMULATION PARAMETERS
# --------------------------------------------------

st.sidebar.header("Simulation parameters")

initial_price = st.sidebar.number_input(
    "Initial price (S₀)",
    min_value=1.0,
    value=100.0,
)

drift = st.sidebar.slider(
    "Drift (μ)",
    min_value=0.0,
    max_value=0.20,
    value=0.05,
    step=0.01,
)

volatility = st.sidebar.slider(
    "Volatility (σ)",
    min_value=0.01,
    max_value=1.0,
    value=0.20,
    step=0.01,
)

maturity = st.sidebar.slider(
    "Maturity (years)",
    min_value=0.25,
    max_value=5.0,
    value=1.0,
    step=0.25,
)

n_steps = st.sidebar.select_slider(
    "Time steps",
    options=[12, 52, 100, 252, 500],
    value=252,
)

n_paths = st.sidebar.select_slider(
    "Number of paths",
    options=[100, 500, 1000, 5000, 10000],
    value=1000,
)


# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

if st.sidebar.button("Run simulation", type="primary"):

    paths = simulate_gbm(
        initial_prices=np.array([initial_price]),
        drift=np.array([drift]),
        volatility=np.array([volatility]),
        correlation=np.array([[1.0]]),
        maturity=maturity,
        n_steps=n_steps,
        n_paths=n_paths,
        seed=42,
    )

    terminal_prices = paths[:, -1, 0]
    time_grid = np.linspace(0, maturity, n_steps + 1)

    # Theoretical moments

    theoretical_mean = initial_price * np.exp(
        drift * maturity
    )

    theoretical_variance = (
        initial_price**2
        * np.exp(2 * drift * maturity)
        * (np.exp(volatility**2 * maturity) - 1)
    )

    theoretical_std = np.sqrt(theoretical_variance)

    empirical_mean = np.mean(terminal_prices)
    empirical_variance = np.var(terminal_prices, ddof=1)
    empirical_std = np.std(terminal_prices, ddof=1)

    # --------------------------------------------------
    # SUMMARY STATISTICS
    # --------------------------------------------------

    st.header("Simulation results")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Initial price",
        f"{initial_price:.2f}",
    )

    col2.metric(
        "Mean terminal price",
        f"{empirical_mean:.2f}",
        delta=f"{empirical_mean - theoretical_mean:+.2f}",
    )

    col3.metric(
        "Median terminal price",
        f"{np.median(terminal_prices):.2f}",
    )

    col4.metric(
        "Terminal standard deviation",
        f"{empirical_std:.2f}",
    )

    # --------------------------------------------------
    # SIMULATED PATHS
    # --------------------------------------------------

    st.subheader("Simulated price trajectories")

    n_display = min(100, n_paths)

    df_paths = pd.DataFrame(
        paths[:n_display, :, 0].T,
        index=time_grid,
    )

    df_paths.index.name = "Time (years)"

    df_paths.columns = [
        f"Path {i + 1}" for i in range(n_display)
    ]

    fig_paths = px.line(
        df_paths,
        labels={
            "value": "Asset price",
            "variable": "Trajectory",
        },
        title=f"First {n_display} simulated paths",
    )

    st.plotly_chart(
        fig_paths,
        use_container_width=True,
    )

    # --------------------------------------------------
    # TERMINAL PRICE DISTRIBUTION
    # --------------------------------------------------

    st.subheader("Terminal price distribution")

    df_terminal = pd.DataFrame({
        "Terminal price": terminal_prices
    })

    fig_hist = px.histogram(
        df_terminal,
        x="Terminal price",
        nbins=50,
        title="Distribution of terminal prices",
    )

    fig_hist.add_vline(
        x=theoretical_mean,
        line_dash="dash",
        annotation_text="Theoretical mean",
    )

    st.plotly_chart(
        fig_hist,
        use_container_width=True,
    )

    # --------------------------------------------------
    # EMPIRICAL VS THEORETICAL MOMENTS
    # --------------------------------------------------

    st.subheader("Empirical vs theoretical moments")

    comparison = pd.DataFrame(
        {
            "Empirical": [
                empirical_mean,
                empirical_variance,
                empirical_std,
            ],
            "Theoretical": [
                theoretical_mean,
                theoretical_variance,
                theoretical_std,
            ],
        },
        index=[
            "Expected price",
            "Variance",
            "Standard deviation",
        ],
    )

    st.dataframe(
        comparison.style.format("{:.4f}"),
        use_container_width=True,
    )

    # --------------------------------------------------
    # THEORETICAL VALUES AND FORMULAS
    # --------------------------------------------------

    with st.expander("Theoretical values and formulas"):

        st.latex(
            r"\mathbb{E}[S_T]=S_0e^{\mu T}"
        )

        st.write(
            f"Theoretical expected price: "
            f"{theoretical_mean:.4f}"
        )

        st.latex(
            r"\mathrm{Var}(S_T)="
            r"S_0^2e^{2\mu T}(e^{\sigma^2T}-1)"
        )

        st.write(
            f"Theoretical variance: "
            f"{theoretical_variance:.4f}"
        )

else:

    st.info(
        "Configure the parameters in the sidebar, "
        "then click Run simulation."
    )
