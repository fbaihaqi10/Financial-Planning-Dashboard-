"""
Corporate Dark Theme
Financial Planning Dashboard
"""

import streamlit as st


CUSTOM_CSS = """
<style>

/* =========================================================
   GLOBAL
========================================================= */
.stApp {
    background: linear-gradient(
        135deg,
        #041b2d 0%,
        #05253d 50%,
        #031726 100%
    );
    color: #F3F7FA;
}

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 95%;
}

/* =========================================================
   SIDEBAR
========================================================= */
section[data-testid="stSidebar"] {
    background: #08233b;
    border-right: 1px solid rgba(45,212,191,0.15);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* =========================================================
   HEADER
========================================================= */
h1 {
    color: white !important;
    font-size: 3rem !important;
    font-weight: 800 !important;
    margin-bottom: 0.5rem !important;
    border-bottom: 4px solid #2DD4BF;
    padding-bottom: 0.4rem;
}

h2 {
    color: white !important;
    font-weight: 700 !important;
}

h3 {
    color: #E7EFF6 !important;
    font-weight: 600 !important;
}

p {
    color: #D6E4EE;
}

/* =========================================================
   KPI CARD
========================================================= */
div[data-testid="stMetric"] {

    background: linear-gradient(
        145deg,
        #17395c,
        #0f2740
    );

    border: 1px solid rgba(45,212,191,0.25);

    border-left: 5px solid #2DD4BF;

    border-radius: 16px;

    padding: 18px;

    box-shadow:
        0 4px 15px rgba(0,0,0,0.30);

    transition: all 0.25s ease;
}

div[data-testid="stMetric"]:hover {

    transform: translateY(-3px);

    box-shadow:
        0 10px 25px rgba(0,0,0,0.45);
}

/* Label */
div[data-testid="stMetricLabel"] {

    color: #9DB7C8 !important;

    font-size: 14px !important;

    font-weight: 500;

    white-space: normal !important;
}

/* Value */
div[data-testid="stMetricValue"] {

    color: white !important;

    font-size: 22px !important;

    font-weight: 800 !important;

    white-space: normal !important;
}

/* Delta */
div[data-testid="stMetricDelta"] {

    color: #4ADE80 !important;

    font-size: 13px !important;

    font-weight: 600 !important;
}

/* =========================================================
   BUTTON
========================================================= */
.stButton>button {

    width: 100%;

    border-radius: 10px;

    border: none;

    background: #2DD4BF;

    color: #041b2d;

    font-weight: 700;
}

.stButton>button:hover {

    background: #3DE8D0;

    color: black;
}

/* =========================================================
   DATAFRAME
========================================================= */
div[data-testid="stDataFrame"] {

    border-radius: 12px;

    border: 1px solid rgba(255,255,255,0.10);

    overflow: hidden;
}

/* =========================================================
   EXPANDER
========================================================= */
div[data-testid="stExpander"] {

    border: 1px solid rgba(255,255,255,0.10);

    border-radius: 12px;

    overflow: hidden;
}

/* =========================================================
   TAB
========================================================= */
button[data-baseweb="tab"] {

    color: white !important;
}

button[data-baseweb="tab"][aria-selected="true"] {

    background: rgba(45,212,191,0.15);

    border-radius: 8px;
}

/* =========================================================
   SCROLLBAR
========================================================= */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #08233b;
}

::-webkit-scrollbar-thumb {
    background: #2DD4BF;
    border-radius: 20px;
}

/* =========================================================
   HR
========================================================= */
hr {
    border-color: rgba(255,255,255,0.10);
}

/* =========================================================
   HIDE STREAMLIT FOOTER
========================================================= */
footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

/* =========================================================
   METRIC TEXT WRAP FIX
========================================================= */
div[data-testid="stMetric"] * {
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: unset !important;
}

</style>
"""


def inject_style():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
