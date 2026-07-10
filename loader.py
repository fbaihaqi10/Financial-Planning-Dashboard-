"""
Loader untuk file '05. Financial Dashboard FPF.xlsx'.
"""

import pandas as pd

from config.settings import (
    EXCEL_FILE,
    SHEET_STMT_INCOME,
    SHEET_VARIANCE_UNIT,
    SHEET_COGS_COMP,
    SHEET_SEASONALITY,
    SHEET_KOMPARASI_PL,
    SHEET_SELLING_PRICE,
    SHEET_COGS_PRICE,
    SHEET_VOLUME_VAR,
    UNIT_BISNIS,
)


def get_workbook():
    return pd.ExcelFile(EXCEL_FILE)


def get_sheet_names():
    return get_workbook().sheet_names


def _raw(sheet_name):
    return pd.read_excel(
        EXCEL_FILE,
        sheet_name=sheet_name,
        header=None
    )


def _safe_num(value):
    """
    Konversi ke numerik.
    Nilai seperti:
    - PSO
    - N/A
    - kosong
    - string lain

    akan menjadi NaN dan tidak membuat Streamlit crash.
    """
    return pd.to_numeric(value, errors="coerce")


def _parse_pl_sheet(
    sheet_name,
    name_col,
    value_cols: dict,
    data_start_row
):
    df = _raw(sheet_name)

    rows = []

    for i in range(data_start_row, len(df)):

        name = df.iloc[i, name_col]

        if pd.isna(name):
            continue

        row = {
            "item": str(name).strip()
        }

        for out_name, col_idx in value_cols.items():
            row[out_name] = _safe_num(
                df.iloc[i, col_idx]
            )

        rows.append(row)

    return pd.DataFrame(rows)


# ==========================================================
# Statement of Comprehensive Income
# ==========================================================
def load_stmt_income():

    return _parse_pl_sheet(
        SHEET_STMT_INCOME,
        name_col=0,
        value_cols={
            "rkap2026": 1,
            "rkap_seasonality": 2,
            "realisasi": 3,
            "prognosa": 4,
            "pct_c_a": 5,
            "pct_c_b": 6,
            "pct_d_a": 7,
        },
        data_start_row=7,
    )


# ==========================================================
# Komparasi PL
# ==========================================================
def load_komparasi_pl():

    return _parse_pl_sheet(
        SHEET_KOMPARASI_PL,
        name_col=0,
        value_cols={
            "realisasi": 1,
            "prognosa": 2,
            "var_opsen": 3,
            "pct_opsen": 4,
            "var_konsol": 5,
            "pct_konsol": 6,
        },
        data_start_row=5,
    )


# ==========================================================
# Seasonality
# ==========================================================
def load_seasonality():

    df = _raw(SHEET_SEASONALITY)

    rows = []

    for i in range(4, len(df)):

        name = df.iloc[i, 1]

        if pd.isna(name):
            continue

        row = {
            "item": str(name).strip()
        }

        for j, unit in enumerate(UNIT_BISNIS):
            row[unit] = _safe_num(
                df.iloc[i, 2 + j]
            )

        rows.append(row)

    return pd.DataFrame(rows)


# ==========================================================
# COGS Composition
# ==========================================================
def load
