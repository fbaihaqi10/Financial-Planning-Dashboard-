import streamlit as st
from style import inject_style

st.set_page_config(
    page_title="Financial Planning & Forecasting Dashboard",
    page_icon="📊",
    layout="wide",
)
inject_style()

st.title("📊 Financial Planning Dashboard")
st.caption("Analisis Varian P&L — Prognosa Mei 2026 vs Realisasi Ytd Mei 2026")

st.markdown("""
Gunakan menu di **sidebar kiri** untuk membuka setiap halaman analisis:

- **Executive Summary** — ringkasan KPI utama & perbandingan P&L
- **Revenue** — kontribusi revenue per unit bisnis & efek harga jual
- **EBITDA** — realisasi EBITDA vs RKAP & prognosa
- **Gross Profit** — laba kotor per unit bisnis & komposisi COGS
- **Net Profit** — alur laba dari laba kotor sampai laba bersih
- **Volume** — variance volume per unit bisnis & per produk

Seluruh nilai finansial ditampilkan dalam **US$ Juta** untuk kemudahan pembacaan,
kecuali disebutkan lain pada tiap chart.
""")
