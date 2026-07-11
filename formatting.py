import pandas as pd


def ribu_to_juta(values):
    try:
        return [v / 1000 if pd.notna(v) else v for v in values]
    except TypeError:
        return values / 1000


def format_df(
    df: pd.DataFrame,
    decimals: int = 2,
    exclude_cols=None
) -> pd.DataFrame:

    exclude_cols = exclude_cols or []

    out = df.copy()

    for col in out.columns:

        if col in exclude_cols:
            continue

        if pd.api.types.is_numeric_dtype(out[col]):

            out[col] = out[col].map(
                lambda v: f"{v:,.{decimals}f}"
                if pd.notna(v)
                else "-"
            )

        else:

            coerced = pd.to_numeric(
                out[col],
                errors="coerce"
            )

            if coerced.notna().mean() >= 0.5:

                out[col] = coerced.map(
                    lambda v: f"{v:,.{decimals}f}"
                    if pd.notna(v)
                    else "-"
                )

    return out
