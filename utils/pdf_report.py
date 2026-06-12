from io import BytesIO
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    Image
)

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER


def generate_pdf_report(
    total_revenue,
    total_transaksi,
    total_qty,
    avg_order,
    insights,
    logo_path=None,
    chart_images=None
):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=26,
        textColor=colors.HexColor("#1E5FD8"),
        alignment=TA_CENTER,
        spaceAfter=14
    )

    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Heading2"],
        fontSize=15,
        textColor=colors.HexColor("#4B5563"),
        alignment=TA_CENTER,
        spaceAfter=10
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading1"],
        fontSize=17,
        textColor=colors.HexColor("#1E5FD8"),
        spaceBefore=10,
        spaceAfter=12
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15
    )

    center_style = ParagraphStyle(
        "CenterStyle",
        parent=styles["BodyText"],
        fontSize=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#6B7280")
    )

    content = []

    # =========================
    # PAGE 1 - COVER
    # =========================
    content.append(Spacer(1, 40))

    if logo_path:
        content.append(Image(logo_path, width=120, height=120))
        content.append(Spacer(1, 20))

    content.append(Paragraph("TOLERANSI KOPI", title_style))
    content.append(Paragraph("Sales Analytics Executive Report", subtitle_style))
    content.append(Spacer(1, 20))

    cover_data = [
        ["Outlet", "Toleransi Kopi Palagan"],
        ["Jenis Laporan", "Analisis Data Transaksi Penjualan"],
        ["Tanggal Export", datetime.now().strftime("%d %B %Y")]
    ]

    cover_table = Table(cover_data, colWidths=[160, 280])
    cover_table.setStyle(TableStyle([
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D6E4FF")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 10),
    ]))

    content.append(cover_table)
    content.append(Spacer(1, 80))
    content.append(Paragraph(
        "Laporan ini dibuat otomatis melalui aplikasi Toleransi Kopi Sales Analytics.",
        center_style
    ))

    content.append(PageBreak())

    # =========================
    # PAGE 2 - EXECUTIVE SUMMARY
    # =========================
    content.append(Paragraph("Executive Summary", heading_style))

    kpi_data = [
        ["Metric", "Value"],
        ["Total Revenue", f"Rp {total_revenue:,.0f}"],
        ["Total Transaksi", f"{total_transaksi:,.0f}"],
        ["Total Item Terjual", f"{total_qty:,.0f}"],
        ["Average Order Value", f"Rp {avg_order:,.0f}"],
    ]

    kpi_table = Table(kpi_data, colWidths=[220, 220])
    kpi_table.setStyle(TableStyle([
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D6E4FF")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 10),
    ]))

    content.append(kpi_table)
    content.append(Spacer(1, 20))

    content.append(Paragraph(
        "Ringkasan ini menampilkan indikator utama performa penjualan, "
        "meliputi total revenue, jumlah transaksi, total item terjual, "
        "dan rata-rata nilai transaksi.",
        normal_style
    ))

    content.append(PageBreak())

    # =========================
    # PAGE 3 - BUSINESS INSIGHTS
    # =========================
    content.append(Paragraph("Business Insights", heading_style))

    if insights:
        for i, insight in enumerate(insights, start=1):
            content.append(Paragraph(f"{i}. {insight}", normal_style))
            content.append(Spacer(1, 8))
    else:
        content.append(Paragraph("Tidak ada insight yang tersedia.", normal_style))

    content.append(PageBreak())

    # =========================
    # PAGE 4+ - CHARTS
    # =========================
    if chart_images:
        for i, (chart_title, chart_buffer) in enumerate(chart_images, start=1):
            content.append(Paragraph(f"Visualisasi {i}: {chart_title}", heading_style))
            content.append(Spacer(1, 8))
            content.append(Image(chart_buffer, width=470, height=260))
            content.append(Spacer(1, 10))
            content.append(Paragraph(
                "Grafik ini digunakan untuk membantu membaca pola penjualan "
                "berdasarkan data transaksi yang telah diproses.",
                normal_style
            ))
            content.append(PageBreak())

    # =========================
    # RECOMMENDATION PAGE
    # =========================
    content.append(Paragraph("Rekomendasi Strategis", heading_style))

    recommendations = [
        "Gunakan produk terlaris sebagai anchor product untuk strategi promosi dan bundling.",
        "Optimalkan stok pada kategori dengan revenue tertinggi agar tidak terjadi kekurangan bahan.",
        "Perkuat kesiapan operasional pada jam dengan revenue tertinggi.",
        "Manfaatkan metode pembayaran paling dominan untuk program promo atau cashback.",
        "Gunakan hasil Apriori untuk membuat paket produk yang sering dibeli bersamaan.",
        "Evaluasi produk dengan kontribusi rendah untuk strategi menu engineering."
    ]

    for i, rec in enumerate(recommendations, start=1):
        content.append(Paragraph(f"{i}. {rec}", normal_style))
        content.append(Spacer(1, 8))

    content.append(PageBreak())

    # =========================
    # CONCLUSION PAGE
    # =========================
    content.append(Paragraph("Kesimpulan", heading_style))

    conclusion = (
        f"Berdasarkan hasil analisis, total revenue yang diperoleh adalah "
        f"Rp {total_revenue:,.0f} dari {total_transaksi:,.0f} transaksi "
        f"dengan total item terjual sebanyak {total_qty:,.0f}. "
        f"Average Order Value tercatat sebesar Rp {avg_order:,.0f}. "
        f"Informasi ini dapat digunakan sebagai dasar dalam pengambilan keputusan "
        f"terkait promosi, pengelolaan stok, evaluasi produk, dan strategi penjualan."
    )

    content.append(Paragraph(conclusion, normal_style))
    content.append(Spacer(1, 30))

    content.append(Paragraph(
        "Generated by Toleransi Kopi Sales Analytics Platform",
        center_style
    ))

    doc.build(content)
    buffer.seek(0)

    return buffer

def generate_premium_executive_report(
    total_revenue,
    total_transaksi,
    total_item,
    aov,
    top_product,
    top_category,
    top_hour,
    top_payment,
    recommendations,
    chart_images=None,
    logo_path=None,
    generated_by="Toleransi Kopi Analytics Platform"
):
    from io import BytesIO
    from datetime import datetime

    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, PageBreak,
        Table, TableStyle, Image
    )
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=40,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()

    blue = colors.HexColor("#1E5FD8")
    dark = colors.HexColor("#111827")
    soft_blue = colors.HexColor("#F1F7FF")
    light_border = colors.HexColor("#D6E4FF")

    title_black = ParagraphStyle(
        "TitleWhite",
        parent=styles["Title"],
        fontSize=28,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=12
    )

    subtitle_black = ParagraphStyle(
        "SubtitleWhite",
        parent=styles["BodyText"],
        fontSize=12,
        textColor=colors.black,
        alignment=TA_CENTER,
        leading=18
    )

    heading = ParagraphStyle(
        "HeadingPremium",
        parent=styles["Heading1"],
        fontSize=18,
        textColor=blue,
        spaceAfter=14
    )

    subheading = ParagraphStyle(
        "SubHeadingPremium",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=dark,
        spaceAfter=8
    )

    body = ParagraphStyle(
        "BodyPremium",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        textColor=dark
    )

    body_center = ParagraphStyle(
        "BodyCenter",
        parent=body,
        alignment=TA_CENTER
    )

    small = ParagraphStyle(
        "Small",
        parent=styles["BodyText"],
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#6B7280")
    )

    def rupiah(value):
        return f"Rp {value:,.0f}".replace(",", ".")

    def clean_text(text):
        return str(text).replace("**", "")

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#6B7280"))
        canvas.drawString(36, 22, "Toleransi Kopi Analytics Platform")
        canvas.drawRightString(560, 22, f"Page {doc.page}")
        canvas.restoreState()

    def cover_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.white)
        canvas.drawCentredString(298, 24, "Generated automatically by Toleransi Kopi Sales Analytics Platform")
        canvas.restoreState()

    content = []

    # =========================
    # COVER PREMIUM
    # =========================
    cover_inner = []

    if logo_path:
        logo = Image(logo_path, width=95, height=95)
        logo_card = Table([[logo]], colWidths=[125], rowHeights=[125])
        logo_card.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOX", (0, 0), (-1, -1), 0.8, colors.white),
            ("ROUNDEDCORNERS", (0, 0), (-1, -1), 14),
        ]))
        cover_inner.append(logo_card)
        cover_inner.append(Spacer(1, 24))

    cover_inner.append(Paragraph("TOLERANSI KOPI ANALYTICS", title_black))
    cover_inner.append(Paragraph("Executive Sales Report Premium", subtitle_black))
    cover_inner.append(Spacer(1, 22))

    cover_info = Table(
        [
            ["Outlet", "Toleransi Kopi Palagan"],
            ["Report Type", "Executive Sales Report"],
            ["Generated Date", datetime.now().strftime("%d %B %Y")],
            ["Generated By", generated_by],
        ],
        colWidths=[140, 300]
    )

    cover_info.setStyle(TableStyle([
        ("TEXTCOLOR", (0, 0), (-1, -1), dark),
        ("GRID", (0, 0), (-1, -1), 0.5, light_border),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 11),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    cover_inner.append(cover_info)
    cover_inner.append(Spacer(1, 35))
    cover_inner.append(Paragraph(
        "A strategic business report designed to support data-driven decision making.",
        subtitle_black
    ))

    cover = Table([[cover_inner]], colWidths=[520], rowHeights=[700])
    cover.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0, blue),
    ]))

    content.append(cover)
    content.append(PageBreak())

    # =========================
    # TABLE OF CONTENTS
    # =========================
    content.append(Paragraph("Table of Contents", heading))

    toc_data = [
        ["01", "Executive Summary"],
        ["02", "KPI Performance"],
        ["03", "AI Business Insight"],
        ["04", "Sales & Product Visualization"],
        ["05", "Operational & Payment Analysis"],
        ["06", "Market Basket Analysis"],
        ["07", "Forecast Summary"],
        ["08", "Strategic Recommendation"],
        ["09", "Conclusion"],
    ]

    toc_table = Table(toc_data, colWidths=[60, 420])
    toc_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), blue),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("BACKGROUND", (1, 0), (1, -1), soft_blue),
        ("GRID", (0, 0), (-1, -1), 0.4, light_border),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 12),
    ]))

    content.append(toc_table)
    content.append(PageBreak())

    # =========================
    # EXECUTIVE SUMMARY
    # =========================
    content.append(Paragraph("01. Executive Summary", heading))

    kpi_table = Table(
        [
            ["Total Revenue", "Total Transaksi", "Item Terjual", "Average Order"],
            [
                rupiah(total_revenue),
                f"{total_transaksi:,.0f}",
                f"{total_item:,.0f}",
                rupiah(aov)
            ]
        ],
        colWidths=[125, 125, 125, 125]
    )

    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), blue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (-1, 1), soft_blue),
        ("TEXTCOLOR", (0, 1), (-1, 1), dark),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.4, light_border),
        ("PADDING", (0, 0), (-1, -1), 13),
    ]))

    content.append(kpi_table)
    content.append(Spacer(1, 20))

    content.append(Paragraph(
        f"Selama periode data yang dianalisis, Toleransi Kopi mencatat total revenue sebesar "
        f"<b>{rupiah(total_revenue)}</b> dari <b>{total_transaksi:,.0f}</b> transaksi. "
        f"Total item terjual mencapai <b>{total_item:,.0f}</b> item dengan Average Order Value sebesar "
        f"<b>{rupiah(aov)}</b>.",
        body
    ))

    content.append(Spacer(1, 14))

    summary_box = Table(
        [[Paragraph(
            f"Produk terlaris adalah <b>{top_product}</b>, kategori terbaik adalah "
            f"<b>{top_category}</b>, jam tersibuk terjadi pada pukul <b>{top_hour}:00</b>, "
            f"dan metode pembayaran dominan adalah <b>{top_payment}</b>.",
            body
        )]],
        colWidths=[500]
    )

    summary_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), soft_blue),
        ("BOX", (0, 0), (-1, -1), 0.5, light_border),
        ("PADDING", (0, 0), (-1, -1), 14),
    ]))

    content.append(summary_box)
    content.append(PageBreak())

    # =========================
    # AI BUSINESS INSIGHT
    # =========================
    content.append(Paragraph("02. AI Business Insight", heading))

    insights = [
        f"Produk {top_product} menjadi produk dengan performa penjualan tertinggi dan dapat dijadikan anchor product untuk strategi promosi.",
        f"Kategori {top_category} menjadi kontributor revenue terbesar, sehingga prioritas stok dan kampanye promosi dapat difokuskan pada kategori ini.",
        f"Jam tersibuk terjadi pada pukul {top_hour}:00. Operasional pada periode ini perlu diperkuat untuk menjaga kualitas layanan.",
        f"Metode pembayaran {top_payment} menjadi metode dominan. Promo berbasis metode pembayaran ini dapat meningkatkan transaksi.",
        "Data ini menunjukkan peluang untuk meningkatkan penjualan melalui bundling produk, optimasi stok, dan penguatan strategi operasional."
    ]

    insight_rows = [["No", "Insight"]]
    for i, insight in enumerate(insights, start=1):
        insight_rows.append([str(i), Paragraph(insight, body)])

    insight_table = Table(insight_rows, colWidths=[40, 460])
    insight_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), blue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (-1, -1), soft_blue),
        ("GRID", (0, 0), (-1, -1), 0.4, light_border),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 9),
    ]))

    content.append(insight_table)
    content.append(PageBreak())

    # =========================
    # VISUALIZATION
    # =========================
    if chart_images:
        for i, (chart_title, chart_buffer) in enumerate(chart_images, start=1):
            content.append(Paragraph(f"0{i + 2}. {chart_title}", heading))
            content.append(Image(chart_buffer, width=500, height=280))
            content.append(Spacer(1, 14))

            chart_insight = (
                "Grafik ini membantu membaca pola performa penjualan dan menjadi dasar "
                "untuk menentukan strategi promosi, operasional, dan evaluasi menu."
            )

            content.append(Paragraph(chart_insight, body))
            content.append(PageBreak())

    # =========================
    # APRIORI PLACEHOLDER
    # =========================
    content.append(Paragraph("07. Market Basket Analysis", heading))

    apriori_box = Table(
        [[Paragraph(
            "Bagian ini digunakan untuk menampilkan hasil Apriori Market Basket Analysis. "
            "Hasil Apriori dapat digunakan untuk menemukan kombinasi produk yang sering dibeli bersamaan "
            "dan menjadi dasar rekomendasi bundling.",
            body
        )]],
        colWidths=[500]
    )

    apriori_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), soft_blue),
        ("BOX", (0, 0), (-1, -1), 0.5, light_border),
        ("PADDING", (0, 0), (-1, -1), 14),
    ]))

    content.append(apriori_box)
    content.append(Spacer(1, 16))

    apriori_sample = Table(
        [
            ["Recommendation", "Business Action"],
            [f"{top_product} + Complementary Product", "Buat paket bundling dan promo upselling di kasir."],
            [f"{top_category} Package", "Fokuskan bundling pada kategori dengan revenue terbesar."],
        ],
        colWidths=[230, 270]
    )

    apriori_sample.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), blue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, light_border),
        ("PADDING", (0, 0), (-1, -1), 10),
    ]))

    content.append(apriori_sample)
    content.append(PageBreak())

    # =========================
    # FORECAST PLACEHOLDER
    # =========================
    content.append(Paragraph("08. Forecast Summary", heading))

    content.append(Paragraph(
        "Bagian forecast digunakan untuk membaca arah potensi penjualan pada periode berikutnya. "
        "Jika tren penjualan menunjukkan pertumbuhan positif, maka stok bahan baku dan kesiapan operasional "
        "perlu disiapkan lebih awal.",
        body
    ))

    content.append(Spacer(1, 14))

    forecast_table = Table(
        [
            ["Forecast Area", "Interpretation"],
            ["Revenue Projection", "Digunakan untuk memperkirakan potensi pendapatan periode berikutnya."],
            ["Stock Planning", "Membantu menentukan kebutuhan stok berdasarkan pola permintaan."],
            ["Operational Planning", "Membantu menentukan kebutuhan staff pada periode sibuk."],
        ],
        colWidths=[180, 320]
    )

    forecast_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), blue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (-1, -1), soft_blue),
        ("GRID", (0, 0), (-1, -1), 0.4, light_border),
        ("PADDING", (0, 0), (-1, -1), 10),
    ]))

    content.append(forecast_table)
    content.append(PageBreak())

    # =========================
    # STRATEGIC RECOMMENDATION
    # =========================
    content.append(Paragraph("09. Strategic Recommendation", heading))

    rec_rows = [["Priority", "Recommendation"]]
    for i, rec in enumerate(recommendations, start=1):
        priority = "High" if i <= 3 else "Medium"
        rec_rows.append([priority, Paragraph(clean_text(rec), body)])

    rec_table = Table(rec_rows, colWidths=[80, 420])
    rec_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), blue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (-1, -1), soft_blue),
        ("GRID", (0, 0), (-1, -1), 0.4, light_border),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 9),
    ]))

    content.append(rec_table)
    content.append(PageBreak())

    # =========================
    # CONCLUSION
    # =========================
    content.append(Paragraph("10. Conclusion", heading))

    conclusion = (
        f"Berdasarkan hasil analisis, Toleransi Kopi memiliki peluang untuk meningkatkan performa bisnis "
        f"melalui optimalisasi produk {top_product}, penguatan kategori {top_category}, dan kesiapan operasional "
        f"pada pukul {top_hour}:00. Executive Report ini dapat digunakan sebagai dasar pengambilan keputusan "
        f"terkait promosi, stok, bundling, evaluasi produk, dan strategi operasional."
    )

    content.append(Paragraph(conclusion, body))
    content.append(Spacer(1, 24))
    content.append(Paragraph(
        "Generated by Toleransi Kopi Sales Analytics Platform",
        body_center
    ))

    content.append(PageBreak())

    # =========================
    # BACK COVER
    # =========================
    back_cover_inner = [
        Paragraph("THANK YOU", title_black),
        Spacer(1, 20),
        Paragraph("Toleransi Kopi Sales Analytics Platform", subtitle_black),
        Spacer(1, 14),
        Paragraph("Data-driven insight for better business decisions.", subtitle_black),
    ]

    back_cover = Table([[back_cover_inner]], colWidths=[520], rowHeights=[700])
    back_cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), blue),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    content.append(back_cover)

    doc.build(
        content,
        onFirstPage=cover_footer,
        onLaterPages=footer
    )

    buffer.seek(0)
    return buffer