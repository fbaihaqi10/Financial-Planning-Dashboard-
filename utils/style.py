"""
CSS kustom untuk mempercantik tampilan default Streamlit:
KPI card lebih menonjol, header dengan garis aksen, tabel lebih rapi.
Panggil inject_style() di baris paling atas tiap halaman (setelah import).
"""

import streamlit as st

CUSTOM_CSS = """
<style>
/* ---- KPI card (st.metric) jadi kartu dengan border & aksen kiri ---- */
div[data-testid="stMetric"] {
    background: linear-gradient(160deg, #16324F, #0F2740);
    border: 1px solid rgba(45, 212, 191, 0.18);
    border-left: 4px solid #2DD4BF;
    border-radius: 10px;
    padding: 14px 18px 10px 18px;
}
/* Streamlit default memotong teks metric (nowrap + ellipsis) -- kita matikan itu total */
div[data-testid="stMetric"] * {
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: unset !important;
}
div[data-testid="stMetricLabel"] {
    font-size: 12.5px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #93AAC0 !important;
    line-height: 1.3;
    min-height: 32px;
}
div[data-testid="stMetricValue"] {
    font-size: 21px !important;
    font-weight: 700;
    line-height: 1.25;
}
div[data-testid="stMetricDelta"] {
    font-size: 12px;
}

/* ---- Judul halaman ---- */
h1 {
    font-weight: 800 !important;
    padding-bottom: 4px;
    border-bottom: 3px solid #2DD4BF;
    display: inline-block;
}

/* ---- Subheader jadi lebih tegas ---- */
h2, h3 {
    font-weight: 700 !important;
    color: #E7EFF6 !important;
}

/* ---- Divider lebih tipis & lembut ---- */
hr {
    border-color: rgba(126,178,209,0.18) !important;
}

/* ---- Expander lebih rapi seperti panel ---- */
div[data-testid="stExpander"] {
    border: 1px solid rgba(126,178,209,0.18);
    border-radius: 10px;
}

/* ---- Sidebar sedikit lebih gelap dari main area ---- */
section[data-testid="stSidebar"] {
    border-right: 1px solid rgba(126,178,209,0.14);
}

/* ---- Dataframe/tabel: header lebih jelas ---- */
div[data-testid="stDataFrame"] {
    border: 1px solid rgba(126,178,209,0.16);
    border-radius: 8px;
}
</style>
"""


def inject_style():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
