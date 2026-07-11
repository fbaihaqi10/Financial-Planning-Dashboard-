"""
Helper format angka: menambahkan pemisah ribuan (koma) pada tabel yang ditampilkan
lewat st.dataframe(), supaya 200000.123 tampil sebagai 200,000.123.
"""

import pandas as pd


def ribu_to_juta(values):
    """Konversi nilai US$ Ribu -> US$ Juta (bagi 1000), dipakai untuk chart/KPI
    supaya angka lebih ringkas dan mudah dibaca oleh manajemen (mis. 20,447,027 Ribu -> 20,447.0 Juta)."""
    try:
        return [v / 1000 if pd.notna(v) else v for v in values]
    except TypeError:
        return values / 1000


def format_df(df: pd.DataFrame, decimals: int = 2, exclude_cols=None) -> pd.DataFrame:
    """
    Kembalikan salinan dataframe dengan seluruh kolom numerik diformat jadi string
    ber-pemisah-ribuan, misal 200000.123 -> "200,000.12".
    Kolom teks (nama item/produk/unit/customer) tidak disentuh.

    Beberapa sheet Excel sumber punya sel berisi tanda "-" untuk nilai kosong
    (bukan 0), yang membuat kolom itu terbaca pandas sebagai tipe campuran
    (object) alih-alih murni angka. Kolom seperti ini tetap diformat --
    sel yang memang bukan angka ditampilkan sebagai "-".
    """
    exclude_cols = exclude_cols or []
    out = df.copy()
    for col in out.columns:
        if col in exclude_cols:
            continue
        if pd.api.types.is_numeric_dtype(out[col]):
            out[col] = out[col].map(
                lambda v: f"{v:,.{decimals}f}" if pd.notna(v) else "-"
            )
        else:
            # Coba paksa jadi angka; sel yang gagal dikonversi (mis. "-") jadi NaN
            coerced = pd.to_numeric(out[col], errors="coerce")
            if coerced.notna().mean() >= 0.5:  # mayoritas isinya angka -> anggap kolom angka
                out[col] = coerced.map(
                    lambda v: f"{v:,.{decimals}f}" if pd.notna(v) else "-"
                )
    return out
