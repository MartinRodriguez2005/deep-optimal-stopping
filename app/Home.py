
import streamlit as st


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Deep Optimal Stopping",
    page_icon="📈",
    layout="wide",
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("Deep Optimal Stopping")

st.markdown(
    """
    ### Numerical methods and deep learning for option pricing

    A quantitative finance research project exploring numerical
    methods, stochastic processes and machine learning techniques
    for the valuation of financial derivatives.
    """
)

st.divider()

# --------------------------------------------------
# PROJECT OVERVIEW
# --------------------------------------------------

st.header("Project Overview")

st.markdown(
    """
    The objective of this project is to implement, analyze and compare
    different numerical approaches to financial derivative pricing.

    Particular attention is given to **optimal stopping problems**,
    which arise in the valuation of American and Bermudan options.

    The project progressively combines:
    - Stochastic calculus and probability theory.
    - Monte Carlo simulation methods.
    - Numerical optimization and regression.
    - Deep learning with PyTorch.
    - Quantitative model evaluation.
    """
)

# --------------------------------------------------
# MODULES
# --------------------------------------------------

st.header("Available Modules")

col1, col2 = st.columns(2)

with col1:
    st.subheader("01 — GBM Simulation")

    st.markdown(
        """
        **Stochastic Process Simulation**

        Simulation of Geometric Brownian Motion paths.

        Topics:
        - Brownian motion.
        - Geometric Brownian Motion.
        - Monte Carlo simulation.
        - Statistical moment validation.
        """
    )

st.page_link(
    "pages/1_GBM_Simulation.py",
    label="Open GBM Simulation",
    icon="📈"
)



with col2:
    st.subheader("02 — Analytical Pricing")

    st.markdown(
        """
        **Closed-form Derivative Valuation**

        Analytical pricing models for financial derivatives.

        Topics:
        - Black–Scholes European options.
        - Forward contracts.
        - Price sensitivity analysis.
        - Theoretical valuation.
        """
    )

st.page_link(
    "pages/2_Analytical_Pricing.py",
    label="Open Analytical Pricing",
    icon="📊"
)

st.divider()

# --------------------------------------------------
# RESEARCH ROADMAP
# --------------------------------------------------

st.header("Research Roadmap")

roadmap = [
    ("01", "Stochastic Processes", "GBM simulation and Monte Carlo methods.", "Completed"),
    ("02", "Analytical Pricing", "Black–Scholes and Forward contracts.", "Completed"),
    ("03", "Longstaff–Schwartz", "Regression-based American option pricing.", "Planned"),
    ("04", "Deep Optimal Stopping", "Neural networks for optimal stopping.", "Planned"),
    ("05", "Model Evaluation", "Convergence, accuracy and computational performance.", "Planned"),
]

for number, title, description, status in roadmap:
    col1, col2, col3 = st.columns([0.6, 3, 1])

    col1.markdown(f"**{number}**")
    col2.markdown(f"**{title}**")
    col2.caption(description)
    col3.caption(status)

    st.divider()

# --------------------------------------------------
# TECHNICAL STACK
# --------------------------------------------------

st.header("Technical Stack")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Language", "Python")
col2.metric("Numerical Computing", "NumPy / SciPy")
col3.metric("Machine Learning", "PyTorch")
col4.metric("Interface", "Streamlit")

st.caption(
    "Research and implementation project — Quantitative Finance."
)
