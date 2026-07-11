"""
Generator PDF ringkasan eksekutif, dibuat pakai fpdf2 (ringan, tanpa dependency berat).
Install dulu: pip install fpdf2
"""

from datetime import datetime
from fpdf import FPDF

TEAL_RGB = (15, 163, 163)
DARK_RGB = (20, 40, 60)
GRAY_RGB = (110, 110, 110)


class DashboardPDF(FPDF):
    def header(self):
        self.set_fill_color(*DARK_RGB)
        self.rect(0, 0, self.w, 22, style="F")
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 15)
        self.set_xy(10, 6)
        self.cell(0, 10, "Financial Planning Dashboard - Executive Report", ln=True)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(230, 230, 230)
        self.set_xy(10, 14)
        self.cell(0, 6, f"Periode: Ytd Mei 2026  |  Dibuat: {datetime.now().strftime('%d %B %Y, %H:%M')}")
        self.ln(18)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Halaman {self.page_no()}", align="C")

    def section_title(self, text):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*DARK_RGB)
        self.set_fill_color(*TEAL_RGB)
        self.cell(3, 8, "", fill=True)
        self.cell(4)
        self.cell(0, 8, text, ln=True)
        self.ln(1)

    def kpi_row(self, items):
        """items: list of (label, value_str, delta_str)"""
        self.set_font("Helvetica", "", 9)
        col_w = (self.w - 20) / len(items)
        y0 = self.get_y()
        for label, value, delta in items:
            x = self.get_x()
            self.set_fill_color(240, 248, 248)
            self.rect(x, y0, col_w - 3, 20, style="F")
            self.set_xy(x + 2, y0 + 2)
            self.set_text_color(*GRAY_RGB)
            self.set_font("Helvetica", "", 7.5)
            self.cell(col_w - 6, 4, label)
            self.set_xy(x + 2, y0 + 7)
            self.set_text_color(*DARK_RGB)
            self.set_font("Helvetica", "B", 11)
            self.cell(col_w - 6, 6, value)
            self.set_xy(x + 2, y0 + 14)
            self.set_font("Helvetica", "", 8)
            self.set_text_color(*TEAL_RGB)
            self.cell(col_w - 6, 4, delta)
            self.set_xy(x + col_w, y0)
        self.set_xy(10, y0 + 24)

    def table(self, headers, rows, col_widths=None):
        n = len(headers)
        col_widths = col_widths or [(self.w - 20) / n] * n
        self.set_font("Helvetica", "B", 8.5)
        self.set_fill_color(*DARK_RGB)
        self.set_text_color(255, 255, 255)
        for h, w in zip(headers, col_widths):
            self.cell(w, 7, str(h), border=1, fill=True, align="C")
        self.ln()
        self.set_font("Helvetica", "", 8)
        self.set_text_color(30, 30, 30)
        fill = False
        for row in rows:
            if self.get_y() > self.h - 25:
                self.add_page()
            self.set_fill_color(245, 250, 250) if fill else self.set_fill_color(255, 255, 255)
            for val, w in zip(row, col_widths):
                align = "L" if isinstance(val, str) and not val.replace(",", "").replace(".", "").replace("-", "").replace("%", "").isdigit() else "R"
                self.cell(w, 6, str(val), border=1, fill=True, align=align)
            self.ln()
            fill = not fill


def _fmt(v, decimals=1):
    try:
        return f"{v:,.{decimals}f}"
    except (TypeError, ValueError):
        return str(v)


def build_executive_pdf(stmt_df, kp_df, output_path):
    """
    Bangun PDF ringkasan eksekutif dari dataframe stmt_income & komparasi_pl.
    Kembalikan path file yang dihasilkan.
    """
    pdf = DashboardPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # ---- KPI utama ----
    pdf.section_title("Ringkasan KPI Utama (Realisasi Ytd Mei 2026, Satuan: US$ Juta)")
    kpi_names = ["Pendapatan Usaha", "Laba/(Rugi) Kotor", "Laba/(Rugi) Usaha", "EBITDA", "Laba/(Rugi) Bersih"]
    items = []
    for name in kpi_names:
        row = stmt_df[stmt_df["item"] == name]
        if row.empty:
            continue
        r = row.iloc[0]
        delta = (r["pct_c_b"] - 1) * 100
        items.append((name, f"{_fmt(r['realisasi'])} Jt USD", f"{delta:+.1f}% vs RKAP"))
    pdf.kpi_row(items[:5])
    pdf.ln(4)

    # ---- Tabel Statement of Comprehensive Income ----
    pdf.section_title("Statement of Comprehensive Income (Satuan: US$ Juta)")
    headers = ["Komponen", "RKAP 2026", "RKAP Seasonality", "Realisasi", "Prognosa 2026", "% vs RKAP Seasonality"]
    rows = []
    for _, r in stmt_df.iterrows():
        is_ratio = "Margin" in r["item"] or r["item"] == "BOPO"
        if is_ratio:
            rows.append([r["item"], f"{r['rkap2026']*100:.1f}%", f"{r['rkap_seasonality']*100:.1f}%",
                         f"{r['realisasi']*100:.1f}%", f"{r['prognosa']*100:.1f}%", f"{(r['pct_c_b']-1)*100:+.1f}%"])
        else:
            rows.append([r["item"], _fmt(r["rkap2026"]), _fmt(r["rkap_seasonality"]),
                         _fmt(r["realisasi"]), _fmt(r["prognosa"]), f"{(r['pct_c_b']-1)*100:+.1f}%"])
    pdf.table(headers, rows, col_widths=[55, 27, 30, 27, 27, 24])
    pdf.ln(6)

    # ---- Tabel Komparasi P&L (item utama saja, biar tidak kepanjangan) ----
    pdf.add_page()
    pdf.section_title("Komparasi P&L - Komponen Utama (Satuan: US$ Ribu)")
    major_items = [
        "Jumlah penjualan dan pendapatan usaha lainnya",
        "Jumlah beban pokok penjualan dan beban langsung lainnya",
        "LABA KOTOR",
        "JUMLAH BEBAN USAHA",
        "LABA/(RUGI) USAHA ",
        "LABA/(RUGI) TAHUN BERJALAN",
        "EBITDA BUMN",
    ]
    headers2 = ["Komponen P&L", "Realisasi Ytd Mei", "Prognosa Mei 2026", "Variance Konsol", "% Perbandingan"]
    rows2 = []
    for name in major_items:
        row = kp_df[kp_df["item"] == name]
        if row.empty:
            continue
        r = row.iloc[0]
        rows2.append([name, _fmt(r["realisasi"], 0), _fmt(r["prognosa"], 0),
                      _fmt(r["var_konsol"], 0), f"{(r['pct_konsol']-1)*100:+.1f}%"])
    pdf.table(headers2, rows2, col_widths=[70, 32, 32, 32, 24])

    pdf.output(output_path)
    return output_path
