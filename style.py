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

/* ---- Fade-in halus saat halaman/konten dimuat ---- */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}
.block-container {
    padding-bottom: 60px !important;
    animation: fadeInUp 0.35s ease-out;
}

/* ---- KPI Card versi kustom (ikon + badge + progress bar) ---- */
.kpi-card-v2 {
    background: linear-gradient(160deg, #16324F, #0F2740);
    border: 1px solid rgba(45, 212, 191, 0.18);
    border-left: 4px solid #2DD4BF;
    border-radius: 12px;
    padding: 16px 18px 14px;
    margin-bottom: 8px;
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    animation: fadeInUp 0.4s ease-out;
}
.kpi-card-v2:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.35);
    border-color: rgba(45, 212, 191, 0.5);
}
.kpi-card-v2-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.kpi-icon {
    font-size: 20px;
    line-height: 1;
}
.kpi-badge {
    font-size: 10px;
    font-weight: 700;
    padding: 3px 9px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    white-space: nowrap;
}
.kpi-label-v2 {
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #93AAC0;
    margin-bottom: 4px;
}
.kpi-value-v2 {
    font-size: 24px;
    font-weight: 800;
    color: #E7EFF6;
    line-height: 1.2;
    margin-bottom: 10px;
}
.kpi-unit {
    font-size: 13px;
    font-weight: 500;
    color: #93AAC0;
}
.kpi-bar-track {
    width: 100%;
    height: 6px;
    border-radius: 4px;
    background: rgba(147, 170, 192, 0.15);
    overflow: hidden;
    margin-bottom: 5px;
}
.kpi-bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.6s ease;
}
.kpi-bar-caption {
    font-size: 11px;
    color: #93AAC0;
}

/* ---- Legenda warna ---- */
.color-legend {
    display: flex;
    gap: 18px;
    flex-wrap: wrap;
    font-size: 12px;
    color: #93AAC0;
    margin: -6px 0 16px;
}
.legend-dot {
    display: inline-block;
    width: 9px;
    height: 9px;
    border-radius: 50%;
    margin-right: 5px;
}

/* ---- Footer copyright, fixed di bawah tengah, muncul di semua halaman ---- */
.app-footer {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 999;
    text-align: center;
    padding: 6px 12px 8px;
    font-size: 10.5px;
    line-height: 1.4;
    color: rgba(147, 170, 192, 0.75);
    background: rgba(8, 24, 38, 0.85);
    backdrop-filter: blur(4px);
    border-top: 1px solid rgba(126, 178, 209, 0.15);
}
</style>

<div class="app-footer">
    Copyright &copy; 2026. Budget Consolidation.<br>
    Financial Planning &amp; Forecasting<br>
    Subholding Downstream
</div>
"""


def inject_style():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
