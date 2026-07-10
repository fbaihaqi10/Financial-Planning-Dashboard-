import streamlit as st
from loader import load_stmt_income, load_volume_variance, load_variance_unit
from utils.charts import bar_variance
from utils.formatting import format_df, ribu_to_juta
from utils.style import inject_style

inject_style()

st.title("🛢️ Volume")
st.caption("Analisis volume: RKAP (Seasonality) vs Realisasi, per unit bisnis & per produk")

stmt = load_stmt_income()
volume_variance = load_volume_variance()
variance_unit = load_variance_unit()

row = stmt[stmt["item"] == "Volume Opsen (KL)"]
if not row.empty:
    r = row.iloc[0]
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Volume Realisasi Ytd Mei", f"{r['realisasi']:,.0f} KL")
    with c2:
        st.metric("RKAP Seasonality Ytd May", f"{r['rkap_seasonality']:,.0f} KL")
    with c3:
        delta = (r["realisasi"] / r["rkap_seasonality"] - 1) * 100 if r["rkap_seasonality"] else 0
        st.metric("Selisih vs RKAP", f"{delta:+.1f}%")

st.divider()

# ---- Qty Variance per unit bisnis (nilai moneter -> dikonversi ke Juta USD) ----
st.subheader("Qty Variance per Unit Bisnis")
vu = variance_unit[variance_unit["unit"] != "Total"]
fig = bar_variance(vu["unit"], ribu_to_juta(vu["qty_variance"]), height=380)
st.plotly_chart(fig, use_container_width=True)
st.caption("Satuan: US$ Juta (efek volume terhadap value)")

st.divider()

# ---- Over/(Under) volume per produk (satuan KL, TIDAK dikonversi -- ini volume fisik bukan uang) ----
st.subheader("Over/(Under) Volume per Produk")
vv = volume_variance[volume_variance["produk"] != "TOTAL ALL"].sort_values("over_under")
fig2 = bar_variance(vv["produk"], vv["over_under"], height=450, horizontal=True)
st.plotly_chart(fig2, use_container_width=True)
st.caption("Satuan: KL (Kiloliter — volume fisik)")

with st.expander("Lihat data mentah Volume Variance Analysis"):
    st.dataframe(format_df(volume_variance, exclude_cols=["produk", "jenis_customer", "satuan"]), use_container_width=True)
