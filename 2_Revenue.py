import streamlit as st
import pandas as pd

from loader import (
    load_stmt_income,
    load_seasonality,
    load_selling_price,
)

from charts import (
    bar_variance,
)

from formatting import (
    ribu_to_juta,
)

from style import inject_style
from config.settings import UNIT_BISNIS

inject_style()

st.title("💰 Revenue")
st.caption("Revenue Analysis")

# =====================================================
# TEST LOAD DATA
# =====================================================

st.write("Loading Statement Income...")

try:
    stmt = load_stmt_income()
    st.success(f"Statement Income OK ({stmt.shape[0]} rows)")
except Exception as e:
    st.error(f"Statement Income ERROR: {e}")
    st.stop()

st.write("Loading Seasonality...")

try:
    seasonality = load_seasonality()
    st.success(f"Seasonality OK ({seasonality.shape[0]} rows)")
except Exception as e:
    st.error(f"Seasonality ERROR: {e}")
    st.stop()

st.write("Loading Selling Price...")

try:
    selling_price = load_selling_price()
    st.success(f"Selling Price OK ({selling_price.shape[0]} rows)")
except Exception as e:
    st.error(f"Selling Price ERROR: {e}")
    st.stop()

st.divider()

# =====================================================
# KPI REVENUE
# =====================================================

if not stmt.empty:

    row = stmt[
        stmt["item"].astype(str).str.upper()
        == "PENDAPATAN USAHA"
    ]

    if not row.empty:

        r = row.iloc[0]

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Realisasi",
            f"{float(r['realisasi']):,.1f}"
        )

        c2.metric(
            "RKAP Seasonality",
            f"{float(r['rkap_seasonality']):,.1f}"
        )

        c3.metric(
            "Prognosa",
            f"{float(r['prognosa']):,.1f}"
        )

st.divider()

# =====================================================
# REVENUE PER UNIT
# =====================================================

try:

    row = seasonality[
        seasonality["item"].astype(str).str.upper()
        ==
        "JUMLAH PENJUALAN DAN PENDAPATAN USAHA LAINNYA"
    ]

    if not row.empty:

        r = row.iloc[0]

        units = [
            u for u in UNIT_BISNIS
            if u != "KONSOLIDASI"
        ]

        values = []

        for unit in units:
            values.append(r.get(unit, 0))

        fig = bar_variance(
            units,
            ribu_to_juta(values),
            height=400,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

except Exception as e:

    st.error(f"Revenue Chart Error: {e}")

st.divider()

# =====================================================
# SELLING PRICE
# =====================================================

try:

    sp = selling_price.copy()

    st.subheader("Selling Price Data")

    st.dataframe(
        sp.head(20),
        use_container_width=True,
    )

except Exception as e:

    st.error(f"Selling Price Error: {e}")
