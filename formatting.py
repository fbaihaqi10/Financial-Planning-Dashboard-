"""
Utility formatting dashboard.
Aman untuk Streamlit Cloud dan PyArrow.
"""

import pandas as pd
import numpy as np


def ribu_to_juta(values):
    """
    Konversi US$ ribu -> US$ juta.
    """

    try:
        result = []

        for v in values:
            try:
                result.append(float(v) / 1000)
            except Exception:
                result.append(np.nan)

        return result

    except Exception:
        try:
            return pd.to_numeric(
                values,
                errors="coerce"
            ) / 1000
        except Exception:
            return values


def format_df(
    df: pd.DataFrame,
    decimals: int = 2,
    exclude_cols=None
) -> pd.DataFrame:
    """
    Format dataframe menjadi aman untuk Streamlit Cloud.
    Semua output dikonversi menjadi string sehingga
    tidak menimbulkan error Arrow/PyArrow.
    """

    exclude_cols = exclude_cols or []

    out = df.copy()

    for col in out.columns:

        if col in exclude_cols:
            out[col] = out[col].fillna("-").astype(str)
            continue

        numeric_col = pd.to_numeric(
            out[col],
            errors="coerce"
        )

        if numeric_col.notna().sum() > 0:

            out[col] = numeric_col.apply(
                lambda x: (
                    f"{x:,.{decimals}f}"
                    if pd.notna(x)
                    else "-"
                )
            )

        else:

            out[col] = (
                out[col]
                .fillna("-")
                .astype(str)
            )

    return out.astype(str)
