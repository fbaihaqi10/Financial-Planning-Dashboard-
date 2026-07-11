import streamlit as st

# ======================================================
# PAGE CONFIG (HARUS PALING ATAS)
# ======================================================

st.set_page_config(
    page_title="Financial Planning Dashboard",
    page_icon="📊",
    layout="wide",
)

# ======================================================
# TEST IMPORT
# ======================================================

try:
    from style import inject_style
    inject_style()
    style_ok = True
except Exception as e:
    style_ok = False
    st.error(f"Style Error : {e}")

# ======================================================
# HEADER
# ======================================================

st.title("📊 Financial Planning Dashboard")
st.caption("Analisis Varian P&L — Prognosa Mei 2026 vs Realisasi Ytd Mei 2026")

# ======================================================
# SYSTEM CHECK
# ======================================================

st.subheader("System Check")

col1, col2 = st.columns(2)

with col1:
    st.success("✅ Streamlit Running")

    if style_ok:
        st.success("✅ style.py Loaded")
    else:
        st.error("❌ style.py Failed")

with col2:

    try:
        from loader import load_stmt_income
        st.success("✅ loader.py Loaded")
    except Exception as e:
        st.error(f"❌ loader.py : {e}")

    try:
        from charts import bar_variance
        st.success("✅ charts.py Loaded")
    except Exception as e:
        st.error(f"❌ charts.py : {e}")

# ======================================================
# MENU INFO
# ======================================================

st.divider()

st.markdown("""
### 📋 Dashboard Menu

Gunakan menu di sidebar kiri untuk membuka halaman:

- Executive Summary
- Revenue
- EBITDA
- Gross Profit
- Net Profit
- Volume

Dashboard ini mengambil seluruh data dari:

**05. Financial Dashboard FPF.xlsx**
""")

# ======================================================
# TEST EXCEL
# ======================================================

st.divider()

st.subheader("Excel Connection")

try:

    df = load_stmt_income()

    st.success(f"Excel Loaded Successfully ({len(df)} rows)")

    st.dataframe(df.head())

except Exception as e:

    st.error(f"Excel Error : {e}")
