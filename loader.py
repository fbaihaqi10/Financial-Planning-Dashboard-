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
        header=None,
    )


def _safe_num(value):
    return pd.to_numeric(
        value,
        errors="coerce"
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

        if pd.isna(name):
            continue

        row = {
            "item": str(name).strip()
        }

        for out_
