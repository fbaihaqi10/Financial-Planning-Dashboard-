"""
Helper reusable untuk seluruh halaman dashboard: KPI card, palet warna, dan
pembuat bar chart Plotly bergaya konsisten (tema gelap, aksen teal/amber).
"""

import streamlit as st
import plotly.graph_objects as go

# Palet warna utama — energetik tapi tetap profesional untuk dashboard finansial
TEAL = "#2DD4BF"
CORAL = "#F2626B"
SLATE = "#5B9BD5"
AMBER = "#F2A93B"
PURPLE = "#A78BFA"
GREEN = "#34D399"

PALETTE = [TEAL, AMBER, SLATE, CORAL, PURPLE, GREEN, "#F472B6", "#FB923C"]

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", size=13, color="#E7EFF6"),
    margin=dict(t=30, l=10, r=10, b=10),
    legend=dict(orientation="h", y=-0.2),
    xaxis=dict(gridcolor="rgba(126,178,209,0.14)", zerolinecolor="rgba(126,178,209,0.3)"),
    yaxis=dict(gridcolor="rgba(126,178,209,0.14)", zerolinecolor="rgba(126,178,209,0.3)"),
    hoverlabel=dict(bgcolor="#122A41", font_size=13, font_family="Inter, sans-serif"),
)


def kpi_card(label, value, comparison_label=None, comparison_value=None, delta_pct=None, unit=""):
    """Tampilkan 1 KPI card pakai st.metric bawaan Streamlit (sudah otomatis pemisah ribuan lewat ':,')."""
    delta_str = None
    if delta_pct is not None:
        delta_str = f"{delta_pct*100:+.1f}% vs {comparison_label}" if comparison_label else f"{delta_pct*100:+.1f}%"
    st.metric(label=label, value=f"{value:,.1f} {unit}".strip(), delta=delta_str)


def bar_compare(labels, series_a, series_a_name, series_b, series_b_name, height=380, horizontal=False):
    """Bar chart 2 series (misal Realisasi vs Prognosa) untuk perbandingan antar item."""
    fig = go.Figure()
    hover_a = "%{y:,.0f}" if not horizontal else "%{x:,.0f}"
    hover_b = hover_a
    if horizontal:
        fig.add_bar(y=labels, x=series_a, name=series_a_name, orientation="h",
                    marker_color=SLATE, hovertemplate=f"{series_a_name}: {hover_a}<extra></extra>")
        fig.add_bar(y=labels, x=series_b, name=series_b_name, orientation="h",
                    marker_color=TEAL, hovertemplate=f"{series_b_name}: {hover_b}<extra></extra>")
    else:
        fig.add_bar(x=labels, y=series_a, name=series_a_name,
                    marker_color=SLATE, hovertemplate=f"{series_a_name}: {hover_a}<extra></extra>")
        fig.add_bar(x=labels, y=series_b, name=series_b_name,
                    marker_color=TEAL, hovertemplate=f"{series_b_name}: {hover_b}<extra></extra>")
    fig.update_layout(**PLOT_LAYOUT, barmode="group", height=height)
    return fig


def bar_variance(labels, values, height=380, horizontal=False, highlight=None):
    """Bar chart 1 series dengan warna otomatis: teal jika positif, coral jika negatif.
    Kalau `highlight` diisi nama salah satu label, bar itu ditonjolkan warna amber +
    bar lain jadi pudar -- dipakai untuk efek 'drill-down' saat user pilih 1 unit/produk."""
    labels_list = list(labels)
    colors = []
    opacities = []
    for lbl, v in zip(labels_list, values):
        if highlight is not None:
            if lbl == highlight:
                colors.append(AMBER)
                opacities.append(1.0)
            else:
                colors.append(TEAL if v >= 0 else CORAL)
                opacities.append(0.35)
        else:
            colors.append(TEAL if v >= 0 else CORAL)
            opacities.append(1.0)
    fig = go.Figure()
    hover = "%{x:,.0f}" if horizontal else "%{y:,.0f}"
    if horizontal:
        fig.add_bar(y=labels_list, x=values, orientation="h", marker=dict(color=colors, opacity=opacities),
                    hovertemplate=f"{hover}<extra></extra>")
    else:
        fig.add_bar(x=labels_list, y=values, marker=dict(color=colors, opacity=opacities),
                    hovertemplate=f"{hover}<extra></extra>")
    fig.update_layout(**PLOT_LAYOUT, height=height, showlegend=False)
    return fig


def pie_composition(labels, values, height=420):
    """Donut chart pakai palet warna hidup, dengan hover format ribuan."""
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.45,
        marker=dict(colors=PALETTE, line=dict(color="#0B1F30", width=2)),
        hovertemplate="%{label}: %{value:,.0f} (%{percent})<extra></extra>",
        textfont=dict(color="#0B1F30", size=12),
    ))
    fig.update_layout(**PLOT_LAYOUT, height=height)
    return fig
