import pandas as pd
import numpy as np


def ribu_to_juta(values):
    try:
        return [
            float(v) / 1000 if pd.notna(v) else np.nan
            for v in values
        ]
    except Exception:
        return values


def format_df(
    df: pd.DataFrame,
    decimals: int = 2,
    exclude_cols=None
):
    exclude_cols = exclude_cols or []

    out = df.copy()

    for col in out.columns:

        if col in exclude_cols:
            out[col] = out[col].astype(str)
            continue

        numeric = pd.to_numeric(
            out[col],
            errors="coerce"
        )

        if numeric.notna().sum() > 0:

            out[col] = numeric.apply(
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
