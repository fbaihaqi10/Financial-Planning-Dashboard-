import streamlit as st
from utils.loader import load_stmt_income, load_komparasi_pl
from utils.charts import kpi_card, bar_compare
from utils.formatting import ribu_to_juta
from utils.style import inject_style

inject_style()

st.title("📊 Executive Summary")
st.caption("Realisasi Ytd Mei 2026 vs RKAP 2026 (Seasonality) & Prognosa Mei 2026")

stmt = load_stmt_income()
kp = load_komparasi_pl()

if stmt.empty:
    st.warning("Data Statement Income kosong.")
    st.stop()

if kp.empty:
    st.warning("Data Komparasi PL kosong.")
    st.stop()


def get_item(df, name):
    row = df[df["item"].astype(str).str.strip() == name.strip()]
    return row.iloc[0] if not row.empty else None


# ---- Baris KPI utama ----
kpi_names = ["Pendapatan Usaha", "Laba/(Rugi) Kotor", "Laba/(Rugi) Usaha", "EBITDA", "Laba/(Rugi) Bersih"]
cols = st.columns(len(kpi_names))
for col, name in zip(cols, kpi_names):
    row = get_item(stmt, name)
    if row is None:
        continue
    with col:
        kpi_card(
            label=name,
            value=row["realisasi"],
            comparison_label="RKAP",
            delta_pct=row["pct_c_b"] - 1,
            unit="Jt USD",
        )

st.divider()

# ---- Chart: Realisasi vs Prognosa untuk komponen utama P&L (dikonversi ke Juta USD) ----
st.subheader("Realisasi vs Prognosa — Komponen Utama P&L")
items = [
    "Jumlah penjualan dan pendapatan usaha lainnya",
    "Jumlah beban pokok penjualan dan beban langsung lainnya",
    "LABA KOTOR",
    "LABA/(RUGI) TAHUN BERJALAN",
    "EBITDA BUMN",
]
labels = ["Revenue", "COGS", "Laba Kotor", "Laba Bersih", "EBITDA"]
rows = [get_item(kp, it) for it in items]
realisasi = ribu_to_juta([r["realisasi"] if r is not None else 0 for r in rows])
prognosa = ribu_to_juta([r["prognosa"] if r is not None else 0 for r in rows])

if rows:
    fig = bar_compare(
        labels,
        prognosa,
        "Prognosa Mei 2026",
        realisasi,
        "Realisasi Ytd Mei",
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)

st.caption("Satuan: US$ Juta")
