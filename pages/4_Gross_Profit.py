import streamlit as st
from utils.loader import load_stmt_income, load_seasonality, load_cogs_composition
from utils.charts import kpi_card, bar_variance, pie_composition
from utils.formatting import format_df, ribu_to_juta
from utils.style import inject_style
from config.settings import UNIT_BISNIS

inject_style()

st.title("🧾 Gross Profit")
st.caption("Laba Kotor (Revenue dikurangi COGS) — Ytd Mei 2026")

stmt = load_stmt_income()
seasonality = load_seasonality()
cogs_comp = load_cogs_composition()


def get_item(df, name):
    row = df[df["item"] == name]
    return row.iloc[0] if not row.empty else None


gp = get_item(stmt, "Laba/(Rugi) Kotor")
if gp is not None:
    c1, c2, c3 = st.columns(3)
    with c1:
        kpi_card("Laba Kotor Realisasi", gp["realisasi"], "RKAP", delta_pct=gp["pct_c_b"] - 1, unit="Jt USD")
    with c2:
        st.metric("RKAP Seasonality Ytd May", f"{gp['rkap_seasonality']:,.1f} Jt USD")
    with c3:
        st.metric("Prognosa Full Year 2026", f"{gp['prognosa']:,.1f} Jt USD")

st.divider()

# ---- Laba Kotor per unit bisnis (dikonversi ke Juta USD) ----
st.subheader("Laba Kotor per Unit Bisnis")
gp_unit = seasonality[seasonality["item"] == "LABA KOTOR"]
if not gp_unit.empty:
    r = gp_unit.iloc[0]
    units = [u for u in UNIT_BISNIS if u != "KONSOLIDASI"]
    values = ribu_to_juta([r[u] for u in units])
    fig = bar_variance(units, values, height=380)
    st.plotly_chart(fig, use_container_width=True)
st.caption("Satuan: US$ Juta")

st.divider()

# ---- Komposisi COGS (dikonversi ke Juta USD) ----
st.subheader("Komposisi COGS Realisasi (faktor pengurang Laba Kotor)")
filtered = cogs_comp[
    ~cogs_comp["item"].str.contains("Total|Subtotal", case=False, na=False)
    & (cogs_comp["real_value"] != 0)
]
values_juta = ribu_to_juta(filtered["real_value"].abs())
fig2 = pie_composition(filtered["item"], values_juta, height=420)
st.plotly_chart(fig2, use_container_width=True)
st.caption("Satuan: US$ Juta")

with st.expander("Lihat data mentah Komposisi COGS (satuan asli: US$ Ribu)"):
    st.dataframe(format_df(cogs_comp, exclude_cols=["item"]), use_container_width=True)
