import streamlit as st
from loader import load_stmt_income, load_komparasi_pl
from charts import kpi_card, bar_compare
from formatting import format_df, ribu_to_juta
from style import inject_style

inject_style()

st.title("🏦 Net Profit")
st.caption("Laba/(Rugi) Tahun Berjalan — Ytd Mei 2026")

stmt = load_stmt_income()
kp = load_komparasi_pl()


def get_item(df, name):
    row = df[df["item"] == name]
    return row.iloc[0] if not row.empty else None


npf = get_item(stmt, "Laba/(Rugi) Bersih")
margin = get_item(stmt, "Profit Margin")

c1, c2 = st.columns(2)
if npf is not None:
    with c1:
        kpi_card("Laba Bersih Realisasi", npf["realisasi"], "RKAP", delta_pct=npf["pct_c_b"] - 1, unit="Jt USD")
if margin is not None:
    with c2:
        st.metric("Profit Margin", f"{margin['realisasi']*100:.1f}%",
                   delta=f"{(margin['pct_c_b']-1)*100:+.1f}% vs RKAP")

st.divider()

# ---- Alur laba (dikonversi ke Juta USD) ----
st.subheader("Alur Laba: dari Laba Kotor sampai Laba Bersih")
items = [
    "LABA KOTOR",
    "JUMLAH BEBAN USAHA",
    "LABA/(RUGI) USAHA ",
    "Jumlah penghasilan/(beban) lain-lain - bersih",
    "Jumlah beban/(manfaat) pajak penghasilan",
    "LABA/(RUGI) TAHUN BERJALAN",
]
labels = ["Laba Kotor", "Beban Usaha", "Laba Usaha", "Peng./(Beban) Lain", "Pajak", "Laba Bersih"]
rows = [get_item(kp, it) for it in items]
realisasi = ribu_to_juta([r["realisasi"] if r is not None else 0 for r in rows])
prognosa = ribu_to_juta([r["prognosa"] if r is not None else 0 for r in rows])

fig = bar_compare(labels, prognosa, "Prognosa Mei 2026", realisasi, "Realisasi Ytd Mei", height=400)
st.plotly_chart(fig, use_container_width=True)
st.caption("Satuan: US$ Juta")

with st.expander("Lihat data mentah Komparasi P&L (satuan asli: US$ Ribu)"):
    st.dataframe(format_df(kp, exclude_cols=["item"]), use_container_width=True)
