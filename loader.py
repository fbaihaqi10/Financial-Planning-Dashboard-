import streamlit as st
import pandas as pd

from loader import (
    load_stmt_income,
    load_seasonality,
    load_selling_price,
)

from charts import (
    kpi_card,
    bar_variance,
)

from formatting import (
    ribu_to_juta,
)

from style import inject_style
from config.settings import UNIT_BISNIS

# ======================================================
# PAGE SETUP
# ======================================================

inject_style()

st.title("💰 Revenue")
st.caption(
    "Analisis pendapatan usaha: realisasi, kontribusi per unit bisnis, dan efek harga jual"
)

# ======================================================
# LOAD DATA
# ======================================================

try:
    stmt = load_stmt_income()
except Exception as e:
    st.error(f"Gagal load Statement Income: {e}")
    stmt = pd.DataFrame()

try:
    seasonality = load_seasonality()
except Exception as e:
    st.error(f"Gagal load Seasonality: {e}")
    seasonality = pd.DataFrame()

try:
    selling_price = load_selling_price()
except Exception as e:
    st.error(f"Gagal load Selling Price: {e}")
    selling_price = pd.DataFrame()

# ======================================================
# KPI
# ======================================================

if not stmt.empty and "item" in stmt.columns:

    row = stmt[
        stmt["item"]
        .astype(str)
        .str.strip()
        .str.upper()
        == "PENDAPATAN USAHA"
    ]

    if not row.empty:

        r = row.iloc[0]

        c1, c2, c3 = st.columns(3)

        with c1:

            try:
                kpi_card(
                    "Realisasi Ytd Mei",
                    r["realisasi"],
                    "RKAP",
                    delta_pct=float(r["pct_c_b"]) - 1,
                    unit="Jt USD",
                )
            except:
                st.metric(
                    "Realisasi Ytd Mei",
                    f"{float(r['realisasi']):,.1f}"
                )

        with c2:

            st.metric(
                "RKAP Seasonality",
                f"{float(r['rkap_seasonality']):,.1f} Jt USD"
            )

        with c3:

            st.metric(
                "Prognosa 2026",
                f"{float(r['prognosa']):,.1f} Jt USD"
            )

st.divider()

# ======================================================
# REVENUE PER UNIT
# ======================================================

st.subheader("Kontribusi Revenue per Unit Bisnis")

if not seasonality.empty:

    try:

        rev_row = seasonality[
            seasonality["item"]
            .astype(str)
            .str.strip()
            .str.upper()
            ==
            "JUMLAH PENJUALAN DAN PENDAPATAN USAHA LAINNYA"
        ]

        if not rev_row.empty:

            r = rev_row.iloc[0]

            units = [
                u for u in UNIT_BISNIS
                if u != "KONSOLIDASI"
            ]

            values = []

            for unit in units:

                value = r.get(unit, 0)

                if pd.isna(value):
                    value = 0

                values.append(value)

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

        st.warning(
            f"Chart Revenue per Unit gagal dibuat: {e}"
        )

st.caption("Satuan: US$ Juta")

st.divider()

# ======================================================
# SELLING PRICE ANALYSIS
# ======================================================

st.subheader(
    "Efek Harga Jual terhadap Revenue per Produk"
)

if not selling_price.empty:

    try:

        sp = selling_price.copy()

        sp["produk"] = (
            sp["produk"]
            .fillna("")
            .astype(str)
        )

        sp["efek_harga_jual"] = pd.to_numeric(
            sp["efek_harga_jual"],
            errors="coerce"
        ).fillna(0)

        sp = sp[
            sp["produk"].str.upper()
            != "TOTAL ALL"
        ]

        sp = sp.sort_values(
            by="efek_harga_jual"
        )

        fig2 = bar_variance(
            sp["produk"],
            ribu_to_juta(
                sp["efek_harga_jual"]
            ),
            height=500,
            horizontal=True,
        )

        st.plotly_chart(
            fig2,
            use_container_width=True,
        )

    except Exception as e:

        st.warning(
            f"Grafik selling price gagal dibuat: {e}"
        )

st.caption(
    "Satuan: US$ Juta — nilai positif menunjukkan harga jual realisasi lebih tinggi dari RKAP"
)

st.divider()

# ======================================================
# RAW DATA
# ======================================================

with st.expander(
    "Lihat Data Selling Price"
):

    if selling_price.empty:

        st.info("Tidak ada data")

    else:

        safe_df = selling_price.copy()

        safe_df = safe_df.fillna("")

        st.dataframe(
            safe_df,
            use_container_width=True,
        )

# ======================================================
# DEBUG
# ======================================================

with st.expander("Debug Info"):

    st.write("Statement Income:", stmt.shape)

    st.write("Seasonality:", seasonality.shape)

    st.write("Selling Price:", selling_price.shape)
