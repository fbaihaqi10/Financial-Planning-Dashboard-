import streamlit as st
import plotly.graph_objects as go
from utils.loader import load_stmt_income
from utils.charts import kpi_card, PLOT_LAYOUT, TEAL
from utils.formatting import format_df
from utils.style import inject_style

inject_style()

st.title("📈 EBITDA")
st.caption("Earnings Before Interest, Tax, Depreciation & Amortization — Ytd Mei 2026")

stmt = load_stmt_income()


def get_item(df, name):
    row = df[df["item"] == name]
    return row.iloc[0] if not row.empty else None


ebitda = get_item(stmt, "EBITDA")
margin = get_item(stmt, "EBITDA Margin")

c1, c2 = st.columns(2)
if ebitda is not None:
    with c1:
        kpi_card("EBITDA Realisasi", ebitda["realisasi"], "RKAP Seasonality", delta_pct=ebitda["pct_c_b"] - 1, unit="Jt USD")
if margin is not None:
    with c2:
        st.metric("EBITDA Margin", f"{margin['realisasi']*100:.1f}%",
                   delta=f"{(margin['pct_c_b']-1)*100:+.1f}% vs RKAP Seasonality")

st.divider()

st.subheader("EBITDA — RKAP vs Realisasi vs Prognosa")
if ebitda is not None:
    labels = ["RKAP 2026\n(Full Year)", "RKAP 2026\n(Seasonality Ytd May)", "Realisasi\nYtd Mei", "Prognosa\n2026 (Full Year)"]
    values = [ebitda["rkap2026"], ebitda["rkap_seasonality"], ebitda["realisasi"], ebitda["prognosa"]]
    fig = go.Figure(go.Bar(
        x=labels, y=values, marker_color=TEAL,
        hovertemplate="%{y:,.1f} Jt USD<extra></extra>",
        text=[f"{v:,.1f}" for v in values], textposition="outside",
    ))
    fig.update_layout(**PLOT_LAYOUT, height=380)
    st.plotly_chart(fig, use_container_width=True)

st.caption("Satuan: US$ Juta")

with st.expander("Lihat semua rasio & metrik finansial"):
    st.dataframe(format_df(stmt, exclude_cols=["item"]), use_container_width=True)
