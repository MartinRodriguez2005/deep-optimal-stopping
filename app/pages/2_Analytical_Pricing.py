
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from src.pricing.black_scholes import black_scholes_price
from src.pricing.forward import forward_price, forward_value


st.set_page_config(
    page_title="Analytical Pricing",
    page_icon="📊",
    layout="wide",
)

st.title("Analytical Pricing")
st.caption("Closed-form valuation of European derivatives")


# ==================================================
# BLACK-SCHOLES
# ==================================================

tab_bs, tab_forward = st.tabs(
    ["Black–Scholes", "Forward Contract"]
)


with tab_bs:

    st.header("Black–Scholes Model")

    st.markdown(
        "Analytical valuation of European call and put options."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        spot = st.number_input(
            "Spot price (S)",
            min_value=0.01,
            value=100.0,
        )

        strike = st.number_input(
            "Strike price (K)",
            min_value=0.01,
            value=100.0,
        )

    with col2:
        maturity = st.number_input(
            "Maturity (years)",
            min_value=0.0,
            value=1.0,
        )

        rate = st.number_input(
            "Risk-free rate",
            value=0.05,
            step=0.01,
            format="%.4f",
        )

    with col3:
        volatility = st.number_input(
            "Volatility",
            min_value=0.0,
            value=0.20,
            step=0.01,
        )

        dividend = st.number_input(
            "Dividend yield",
            value=0.0,
            step=0.01,
            format="%.4f",
        )

    option_type = st.selectbox(
        "Option type",
        ["call", "put"],
    )

    price = black_scholes_price(
        spot=spot,
        strike=strike,
        maturity=maturity,
        risk_free_rate=rate,
        volatility=volatility,
        option_type=option_type,
        dividend_yield=dividend,
    )

    st.divider()

    st.metric(
        label=f"European {option_type.capitalize()} Price",
        value=f"{price:.4f}",
    )

    st.subheader("Model formula")

    st.latex(
        r"C=S_0e^{-qT}N(d_1)-Ke^{-rT}N(d_2)"
    )

    st.latex(
        r"P=Ke^{-rT}N(-d_2)-S_0e^{-qT}N(-d_1)"
    )

    # ----------------------------------------------
    # OPTION PRICE VS SPOT
    # ----------------------------------------------

    st.divider()
    st.subheader("Option price vs underlying price")

    spot_range = np.linspace(
        max(0.01, spot * 0.5),
        spot * 1.5,
        100,
    )

    prices_spot = [
        black_scholes_price(
            s,
            strike,
            maturity,
            rate,
            volatility,
            option_type,
            dividend,
        )
        for s in spot_range
    ]

    df_spot = pd.DataFrame({
        "Spot price": spot_range,
        "Option price": prices_spot,
    })

    fig_spot = px.line(
        df_spot,
        x="Spot price",
        y="Option price",
        title=f"{option_type.capitalize()} price sensitivity to spot",
    )

    fig_spot.add_vline(
        x=strike,
        line_dash="dash",
        annotation_text="Strike",
    )

    st.plotly_chart(
        fig_spot,
        use_container_width=True,
    )

    # ----------------------------------------------
    # OPTION PRICE VS VOLATILITY
    # ----------------------------------------------

    st.subheader("Option price vs volatility")

    volatility_range = np.linspace(0.01, 1.0, 100)

    prices_volatility = [
        black_scholes_price(
            spot,
            strike,
            maturity,
            rate,
            vol,
            option_type,
            dividend,
        )
        for vol in volatility_range
    ]

    df_volatility = pd.DataFrame({
        "Volatility": volatility_range,
        "Option price": prices_volatility,
    })

    fig_volatility = px.line(
        df_volatility,
        x="Volatility",
        y="Option price",
        title="Option price sensitivity to volatility",
    )

    fig_volatility.add_vline(
        x=volatility,
        line_dash="dash",
        annotation_text="Current volatility",
    )

    st.plotly_chart(
        fig_volatility,
        use_container_width=True,
    )


# ==================================================
# FORWARD CONTRACT
# ==================================================

with tab_forward:

    st.header("Forward Contract")

    st.markdown(
        "Fair delivery price and current valuation of a forward contract."
    )

    col1, col2 = st.columns(2)

    with col1:
        forward_spot = st.number_input(
            "Spot price",
            min_value=0.01,
            value=100.0,
            key="forward_spot",
        )

        forward_maturity = st.number_input(
            "Maturity (years)",
            min_value=0.0,
            value=1.0,
            key="forward_maturity",
        )

    with col2:
        forward_rate = st.number_input(
            "Risk-free rate",
            value=0.05,
            step=0.01,
            format="%.4f",
            key="forward_rate",
        )

        forward_dividend = st.number_input(
            "Dividend yield",
            value=0.0,
            step=0.01,
            format="%.4f",
            key="forward_dividend",
        )

    fair_price = forward_price(
        spot=forward_spot,
        maturity=forward_maturity,
        risk_free_rate=forward_rate,
        dividend_yield=forward_dividend,
    )

    st.divider()

    st.subheader("Fair Forward Price")

    st.metric(
        label="Forward delivery price",
        value=f"{fair_price:.4f}",
    )

    st.latex(
        r"F_{0,T}=S_0e^{(r-q)T}"
    )

    # ----------------------------------------------
    # FORWARD PRICE VS MATURITY
    # ----------------------------------------------

    st.divider()
    st.subheader("Forward price vs maturity")

    maturity_range = np.linspace(0, 10, 100)

    forward_prices = [
        forward_price(
            forward_spot,
            t,
            forward_rate,
            forward_dividend,
        )
        for t in maturity_range
    ]

    df_forward = pd.DataFrame({
        "Maturity (years)": maturity_range,
        "Forward price": forward_prices,
    })

    fig_forward = px.line(
        df_forward,
        x="Maturity (years)",
        y="Forward price",
        title="Forward price term structure",
    )

    fig_forward.add_hline(
        y=forward_spot,
        line_dash="dash",
        annotation_text="Spot price",
    )

    st.plotly_chart(
        fig_forward,
        use_container_width=True,
    )

    # ----------------------------------------------
    # EXISTING FORWARD CONTRACT
    # ----------------------------------------------

    st.divider()
    st.subheader("Existing Forward Contract")

    delivery_price = st.number_input(
        "Contract delivery price (K)",
        min_value=0.01,
        value=float(round(fair_price, 4)),
        key="delivery_price",
    )

    contract_value = forward_value(
        spot=forward_spot,
        delivery_price=delivery_price,
        maturity=forward_maturity,
        risk_free_rate=forward_rate,
        dividend_yield=forward_dividend,
    )

    st.metric(
        label="Current contract value",
        value=f"{contract_value:.4f}",
    )

    st.latex(
        r"V_0=S_0e^{-qT}-Ke^{-rT}"
    )

    # ----------------------------------------------
    # CONTRACT VALUE VS SPOT
    # ----------------------------------------------

    st.subheader("Contract value vs spot price")

    spot_range_forward = np.linspace(
        forward_spot * 0.5,
        forward_spot * 1.5,
        100,
    )

    contract_values = [
        forward_value(
            s,
            delivery_price,
            forward_maturity,
            forward_rate,
            forward_dividend,
        )
        for s in spot_range_forward
    ]

    df_value = pd.DataFrame({
        "Spot price": spot_range_forward,
        "Contract value": contract_values,
    })

    fig_value = px.line(
        df_value,
        x="Spot price",
        y="Contract value",
        title="Forward contract value sensitivity to spot",
    )

    fig_value.add_hline(
        y=0,
        line_dash="dash",
    )

    st.plotly_chart(
        fig_value,
        use_container_width=True,
    )
