"""
Loader untuk file '05. Financial Dashboard FPF.xlsx'.

Setiap sheet Excel punya 1 kolom kosong di paling kiri (kolom A),
jadi semua index kolom di bawah dihitung dari situ.

Semua fungsi load_xxx() mengembalikan pandas.DataFrame.
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


# ======================================================
# HELPER
# ======================================================

def get_workbook():
    return pd.ExcelFile(EXCEL_FILE)


def get_sheet_names():
    return get_workbook().sheet_names


def _raw(sheet_name):
    return pd.read_excel(
        EXCEL_FILE,
        sheet_name=sheet_name,
        header=None,
        engine="openpyxl",
    )


def _parse_pl_sheet(
    sheet_name,
    name_col,
    value_cols,
    data_start_row,
):
    df = _raw(sheet_name)

    rows = []

    for i in range(data_start_row, len(df)):

        name = df.iloc[i, name_col]

        if pd.isna(name) or name == 0:
            continue

        row = {
            "item": str(name).strip()
        }

        for out_name, col_idx in value_cols.items():
            row[out_name] = df.iloc[i, col_idx]

        rows.append(row)

    return pd.DataFrame(rows)


# ======================================================
# 1. STATEMENT OF COMPREHENSIVE INCOME
# ======================================================

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


# ======================================================
# 2. KOMPARASI PL
# ======================================================

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


# ======================================================
# 3. SEASONALITY PER UNIT BISNIS
# ======================================================

def load_seasonality():

    df = _raw(SHEET_SEASONALITY)

    rows = []

    for i in range(4, len(df)):

        item = df.iloc[i, 1]

        if pd.isna(item) or item == 0:
            continue

        row = {
            "item": str(item).strip()
        }

        for j, unit in enumerate(UNIT_BISNIS):
            row[unit] = df.iloc[i, 2 + j]

        rows.append(row)

    return pd.DataFrame(rows)


# ======================================================
# 4. COGS COMPOSITION
# ======================================================

def load_cogs_composition():

    df = _raw(SHEET_COGS_COMP)

    rows = []

    for i in range(5, len(df)):

        item = df.iloc[i, 1]

        if pd.isna(item):
            continue

        rows.append({
            "item": str(item).strip(),

            "rkap_volume": df.iloc[i, 2],
            "rkap_price": df.iloc[i, 3],
            "rkap_value": df.iloc[i, 4],

            "rkapprop_volume": df.iloc[i, 5],
            "rkapprop_price": df.iloc[i, 6],
            "rkapprop_value": df.iloc[i, 7],

            "real_volume": df.iloc[i, 8],
            "real_price": df.iloc[i, 9],
            "real_value": df.iloc[i, 10],
        })

    return pd.DataFrame(rows)


# ======================================================
# 5. VARIANCE UNIT BISNIS
# ======================================================

def load_variance_unit():

    df = _raw(SHEET_VARIANCE_UNIT)

    rows = []

    for i in range(5, len(df)):

        unit = df.iloc[i, 1]

        if pd.isna(unit):
            continue

        rows.append({
            "unit": str(unit).strip(),

            "rkap_volume": df.iloc[i, 2],
            "rkap_price": df.iloc[i, 3],
            "rkap_value": df.iloc[i, 4],

            "real_volume": df.iloc[i, 5],
            "real_price": df.iloc[i, 6],
            "real_value": df.iloc[i, 7],

            "variance_volume": df.iloc[i, 8],
            "variance_value": df.iloc[i, 9],

            "qty_variance": df.iloc[i, 10],
            "price_variance": df.iloc[i, 11],
            "total_variance": df.iloc[i, 12],
        })

    return pd.DataFrame(rows)


# ======================================================
# 6. VOLUME VARIANCE
# ======================================================

def load_volume_variance():

    df = _raw(SHEET_VOLUME_VAR)

    rows = []

    for i in range(7, len(df)):

        produk = df.iloc[i, 2]

        if pd.isna(produk):
            continue

        rows.append({
            "produk": str(df.iloc[i, 2]),
            "jenis_customer": str(df.iloc[i, 3]),
            "satuan": str(df.iloc[i, 4]),

            "volume_rkap": df.iloc[i, 5],
            "volume_realisasi": df.iloc[i, 6],
            "over_under": df.iloc[i, 7],

            "harga_jual_rkap": df.iloc[i, 8],
            "cogs_rkap": df.iloc[i, 9],
            "margin_rkap": df.iloc[i, 10],

            "efek_vol_thd_rev": df.iloc[i, 11],
        })

    return pd.DataFrame(rows)


# ======================================================
# 7. COGS PRICE ANALYSIS
# ======================================================

def load_cogs_price():

    df = _raw(SHEET_COGS_PRICE)

    rows = []

    for i in range(7, len(df)):

        produk = df.iloc[i, 2]

        if pd.isna(produk):
            continue

        rows.append({
            "produk": str(df.iloc[i, 2]),
            "jenis_customer": str(df.iloc[i, 3]),

            "cogs_rkap": df.iloc[i, 4],
            "cogs_realisasi": df.iloc[i, 5],
            "selisih_cogs": df.iloc[i, 6],

            "volume_rkap": df.iloc[i, 7],
            "volume_realisasi": df.iloc[i, 8],

            "efek_harga_thd_cogs": df.iloc[i, 9],
            "efek_volume_thd_cogs": df.iloc[i, 10],
        })

    return pd.DataFrame(rows)


# ======================================================
# 8. SELLING PRICE ANALYSIS
# ======================================================

def load_selling_price():

    df = _raw(SHEET_SELLING_PRICE)

    rows = []

    for i in range(7, len(df)):

        produk = df.iloc[i, 2]

        if pd.isna(produk):
            continue

        rows.append({
            "produk": str(df.iloc[i, 2]),
            "jenis_customer": str(df.iloc[i, 3]),

            "revenue_rkap": df.iloc[i, 4],
            "revenue_realisasi": df.iloc[i, 5],

            "selisih_usdkl": df.iloc[i, 6],
            "volume_realisasi": df.iloc[i, 7],

            "efek_harga_jual": df.iloc[i, 8],
        })

    return pd.DataFrame(rows)
