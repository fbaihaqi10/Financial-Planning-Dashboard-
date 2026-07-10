from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

EXCEL_FILE = BASE_DIR / "05. Financial Dashboard FPF.xlsx"

SHEET_STMT_INCOME   = "Statement of Comprehensive Inco"
SHEET_VARIANCE_UNIT = "Variance PL per Unit Bisnis"
SHEET_COGS_COMP     = "Komposisi COGS Ytd. Mei 2026"
SHEET_SEASONALITY   = "Seasonality PL Unit Bisnis Ytd."
SHEET_KOMPARASI_PL  = "Komparasi PL (Prognosa Mei 2026"
SHEET_SELLING_PRICE = "Selling Price Analysis"
SHEET_COGS_PRICE    = "COGS Price Analysis"
SHEET_VOLUME_VAR    = "Volume Variance Analysis"

UNIT_BISNIS = [
    "FRM",
    "FIM",
    "AVIASI",
    "LPG&GP",
    "PETKIM",
    "TOB",
    "HO C&T",
    "OPSEN",
    "AP + ELIM",
    "KONSOLIDASI",
]
