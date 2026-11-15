
import sys
from pathlib import Path

# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

# --------------------------------------------------
# IMPORTS
# --------------------------------------------------

import streamlit as st

from app.translations import init_language, t

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Deep Optimal Stopping",
    page_icon="📈",
    layout="wide",
)

# Initialize language selector
init_language()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title(t("Deep Optimal Stopping"))

st.markdown(
    f"""
    ### {t("Numerical methods and deep learning for option pricing")}

    {t("A quantitative finance research project exploring numerical methods, stochastic processes and machine learning techniques for the valuation of financial derivatives.")}
    """
)

st.divider()

# --------------------------------------------------
# PROJECT OVERVIEW
# --------------------------------------------------

st.header(t("Project Overview"))

st.markdown(
    f"""
    {t("The objective of this project is to implement, analyze and compare different numerical approaches to financial derivative pricing.")}

    {t("Particular attention is given to optimal stopping problems, which arise in the valuation of American and Bermudan options.")}

    {t("The project progressively combines:")}
    - {t("Stochastic calculus and probability theory.")}
    - {t("Monte Carlo simulation methods.")}
    - {t("Numerical optimization and regression.")}
    - {t("Deep learning with PyTorch.")}
    - {t("Quantitative model evaluation.")}
    """
)

st.divider()

# --------------------------------------------------
# AVAILABLE MODULES
# --------------------------------------------------

st.header(t("Available Modules"))

col1, col2 = st.columns(2)

# --------------------------------------------------
# MODULE 1 — GBM SIMULATION
# --------------------------------------------------

with col1:
    st.subheader(t("01 — GBM Simulation"))

    st.markdown(
        f"""
        **{t("Stochastic Process Simulation")}**

        {t("Simulation of Geometric Brownian Motion paths.")}

        **{t("Topics:")}**
        - {t("Brownian motion.")}
        - {t("Geometric Brownian Motion.")}
        - {t("Monte Carlo simulation.")}
        - {t("Statistical moment validation.")}
        """
    )

    st.page_link(
        "pages/1_GBM_Simulation.py",
        label=t("Open GBM Simulation"),
        icon="📈",
    )

# --------------------------------------------------
# MODULE 2 — ANALYTICAL PRICING
# --------------------------------------------------

with col2:
    st.subheader(t("02 — Analytical Pricing"))

    st.markdown(
        f"""
        **{t("Closed-form Derivative Valuation")}**

        {t("Analytical pricing models for financial derivatives.")}

        **{t("Topics:")}**
        - {t("Black–Scholes European options.")}
        - {t("Forward contracts.")}
        - {t("Price sensitivity analysis.")}
        - {t("Theoretical valuation.")}
        """
    )

    st.page_link(
        "pages/2_Analytical_Pricing.py",
        label=t("Open Analytical Pricing"),
        icon="📊",
    )

st.divider()

# --------------------------------------------------
# RESEARCH ROADMAP
# --------------------------------------------------

st.header(t("Research Roadmap"))

roadmap = [
    (
        "01",
        "Stochastic Processes",
        "GBM simulation and Monte Carlo methods.",
        "Completed",
    ),
    (
        "02",
        "Analytical Pricing",
        "Black–Scholes and Forward contracts.",
        "Completed",
    ),
    (
        "03",
        "Longstaff–Schwartz",
        "Regression-based American option pricing.",
        "Planned",
    ),
    (
        "04",
        "Deep Optimal Stopping",
        "Neural networks for optimal stopping.",
        "Planned",
    ),
    (
        "05",
        "Model Evaluation",
        "Convergence, accuracy and computational performance.",
        "Planned",
    ),
]

for number, title, description, status in roadmap:
    col1, col2, col3 = st.columns([0.6, 3, 1])

    with col1:
        st.markdown(f"**{number}**")

    with col2:
        st.markdown(f"**{t(title)}**")
        st.caption(t(description))

    with col3:
        st.caption(t(status))

    st.divider()

# --------------------------------------------------
# TECHNICAL STACK
# --------------------------------------------------

st.header(t("Technical Stack"))

col1, col2, col3, col4 = st.columns(4)

col1.metric(t("Language"), "Python")
col2.metric(t("Numerical Computing"), "NumPy / SciPy")
col3.metric(t("Machine Learning"), "PyTorch")
col4.metric(t("Interface"), "Streamlit")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.caption(
    t("Research and implementation project — Quantitative Finance.")
)
