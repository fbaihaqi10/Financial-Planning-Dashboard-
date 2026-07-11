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


def kpi_card(label, value, comparison_label=None, comparison_value=None, delta_pct=None, unit="", icon="📊"):
    """
    KPI card custom (bukan st.metric bawaan) dengan:
    - ikon di kiri atas
    - badge status warna (Di Atas / Sesuai / Di Bawah target)
    - progress bar kecil menunjukkan % pencapaian terhadap target
    """
    delta_pct = delta_pct if delta_pct is not None else 0
    achievement = 1 + delta_pct  # realisasi / target

    if delta_pct >= 0.03:
        badge_color, badge_text = TEAL, "Di Atas RKAP"
    elif delta_pct <= -0.03:
        badge_color, badge_text = CORAL, "Di Bawah RKAP"
    else:
        badge_color, badge_text = AMBER, "Sesuai RKAP"

    bar_pct = max(0, min(achievement, 1.3)) / 1.3 * 100  # dinormalisasi, cap tampilan di 130%
    comp_label = comparison_label or "target"

    st.markdown(f"""
    <div class="kpi-card-v2">
      <div class="kpi-card-v2-top">
        <span class="kpi-icon">{icon}</span>
        <span class="kpi-badge" style="background:{badge_color}26;color:{badge_color};border:1px solid {badge_color}66;">{badge_text}</span>
      </div>
      <div class="kpi-label-v2">{label}</div>
      <div class="kpi-value-v2">{value:,.1f}<span class="kpi-unit"> {unit}</span></div>
      <div class="kpi-bar-track"><div class="kpi-bar-fill" style="width:{bar_pct:.0f}%; background:{badge_color};"></div></div>
      <div class="kpi-bar-caption">{achievement*100:.0f}% dari {comp_label}</div>
    </div>
    """, unsafe_allow_html=True)


def color_legend():
    """Legenda kecil menjelaskan arti warna teal/coral/amber, ditaruh di bawah judul halaman."""
    st.markdown(f"""
    <div class="color-legend">
      <span><span class="legend-dot" style="background:{TEAL};"></span> Sesuai / di atas RKAP</span>
      <span><span class="legend-dot" style="background:{AMBER};"></span> Mendekati RKAP</span>
      <span><span class="legend-dot" style="background:{CORAL};"></span> Di bawah RKAP</span>
    </div>
    """, unsafe_allow_html=True)


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
