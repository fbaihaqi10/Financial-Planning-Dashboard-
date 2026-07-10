import streamlit as st

from loader import (
    load_stmt_income,
    load_volume_variance,
    load_variance_unit,
)

from charts import bar_variance
from formatting import format_df, ribu_to_juta
from style import inject_style

inject_style()

st.title("🛢️ Volume")
st.caption(
    "Analisis volume: RKAP (Seasonality) vs Realisasi, "
    "per unit bisnis & per produk"
)

stmt = load_stmt_income()
volume_variance = load_volume_variance()
variance_unit = load_variance_unit()

# ==========================================================
# KPI VOLUME
# ==========================================================
row = stmt[stmt["item"] == "Volume Opsen (KL)"]

if not row.empty:

    r = row.iloc[0]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Volume Realisasi Ytd Mei",
            f"{r['realisasi
