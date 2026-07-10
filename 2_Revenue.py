import streamlit as st
from loader import load_stmt_income, load_seasonality, load_selling_price, load_volume_variance
from charts import kpi_card, bar_variance
from formatting import format_df, ribu_to_juta
from style import inject_style
from config.settings import UNIT_BISNIS

inject_style()

st.title("💰 Revenue")
st.caption("Analisis pendapatan usaha: realisasi, kontribusi per unit bisnis, dan efek harga jual")

stmt = load_stmt_income()
seasonality = load_seasonality()
selling_price = load_selling_price()
volume_variance = load_volume_variance()

row = stmt[stmt["item"] == "Pendapatan Usaha"]
if not row.empty:
    r = row.iloc[0]
    c1, c2, c3 = st.columns(3)
    with c1:
        kpi_card("Realisasi Ytd Mei", r["realisasi"], "RKAP", delta_pct=r["pct_c_b"] - 1, unit="Jt USD")
    with c2:
        st.metric("RKAP 2026 (Seasonality Ytd May)", f"{r['rkap_seasonality']:,.1f} Jt USD")
    with c3:
        st.metric("Prognosa Full Year 2026", f"{r['prognosa']:,.1f} Jt USD")

st.divider()

# ---- Revenue per unit bisnis (dikonversi ke Juta USD) ----
st.subheader("Kontribusi Revenue per Unit Bisnis")
rev_row = seasonality[seasonality["item"] == "Jumlah penjualan dan pendapatan usaha lainnya"]
if not rev_row.empty:
    r = rev_row.iloc[0]
    units = [u for u in UNIT_BISNIS if u != "KONSOLIDASI"]
    values = ribu_to_juta([r[u] for u in units])
    fig = bar_variance(units, values, height=380)
    st.plotly_chart(fig, use_container_width=True)
st.caption("Satuan: US$ Juta")

st.divider()

# ---- Efek harga jual per produk (dikonversi ke Juta USD) ----
st.subheader("Efek Harga Jual terhadap Revenue per Produk")
sp = selling_price[selling_price["produk"] != "TOTAL ALL"].sort_values("efek_harga_jual")
fig2 = bar_variance(sp["produk"], ribu_to_juta(sp["efek_harga_jual"]), height=420, horizontal=True)
st.plotly_chart(fig2, use_container_width=True)
st.caption("Satuan: US$ Juta — nilai positif berarti harga jual realisasi lebih tinggi dari RKAP")

with st.expander("Lihat data mentah Selling Price Analysis (satuan asli: US$ Ribu)"):
    st.dataframe(format_df(selling_price, exclude_cols=["produk", "jenis_customer"]), use_container_width=True)
