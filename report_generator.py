# report_generator.py

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime


styles = getSampleStyleSheet()

# Add new styles safely
styles.add(ParagraphStyle(name="MainTitle", fontSize=22, leading=26, alignment=1, spaceAfter=20))
styles.add(ParagraphStyle(name="SecHeader", fontSize=16, spaceAfter=10, leading=18))
styles.add(ParagraphStyle(name="ChartHeader", fontSize=13, spaceAfter=6, leading=15))
styles.add(ParagraphStyle(name="SummaryText", fontSize=10, textColor=colors.grey))


# -----------------------------------------------------------------------------
# Helper: Two-column chart layout (correct layout)
# -----------------------------------------------------------------------------
def add_chart_row(flow, left_title, left_img, right_title, right_img):

    # left column content
    left_col = [
        Paragraph(f"<b>{left_title}</b>", styles["ChartHeader"]),
        Spacer(1, 4),
        Image(left_img, width=240, height=150)
    ]

    # right column content
    right_col = [
        Paragraph(f"<b>{right_title}</b>", styles["ChartHeader"]),
        Spacer(1, 4),
        Image(right_img, width=240, height=150)
    ]

    # Table row containing 2 cells
    table = Table(
        [[left_col, right_col]],
        colWidths=[260, 260]
    )

    table.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 18),
    ]))

    flow.append(table)
    flow.append(Spacer(1, 10))


# -----------------------------------------------------------------------------
# MAIN PDF CREATOR
# -----------------------------------------------------------------------------
def create_pdf_report(filename, summary_table, dfs, charts):

    chart_map = {title: path for title, path in charts}

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=25,
        rightMargin=25,
        topMargin=25,
        bottomMargin=20
    )

    flow = []

    # -------------------------------------------------------------------------
    # MAIN HEADING (NOW FIXED)
    # -------------------------------------------------------------------------
    flow.append(Paragraph("Sales Analytics Report", styles["MainTitle"]))
    flow.append(Paragraph(f"Generated on {datetime.now().strftime('%d %b %Y %H:%M')}", styles["SummaryText"]))
    flow.append(Spacer(1, 15))

    # -------------------------------------------------------------------------
    # EXECUTIVE SUMMARY
    # -------------------------------------------------------------------------
    flow.append(Paragraph("Executive Summary", styles["SecHeader"]))
    flow.append(Paragraph(
        "This dashboard highlights sales performance across customers, cities, "
        "products and time periods, providing business insights for decision-making.",
        styles["SummaryText"]
    ))
    flow.append(Spacer(1, 12))
    flow.append(summary_table)
    flow.append(Spacer(1, 18))

    # -------------------------------------------------------------------------
    # 2-COLUMN CHART GRID (CORRECTED)
    # -------------------------------------------------------------------------

    add_chart_row(
        flow,
        "Top 10 Customers",
        chart_map["Top 10 Customers"],
        "Monthly Revenue Trend",
        chart_map["Monthly Revenue Trend"]
    )

    add_chart_row(
        flow,
        "City Revenue (>150K)",
        chart_map["City Revenue Bar"],
        "Best Selling Products",
        chart_map["Best Selling Products"]
    )

    add_chart_row(
        flow,
        "City Revenue Share",
        chart_map["City Revenue Pie"],
        "New vs Returning Customers",
        chart_map["New vs Returning Customers"]
    )

    flow.append(Paragraph("<b>Revenue Distribution</b>", styles["ChartHeader"]))
    flow.append(Spacer(1, 4))
    flow.append(Image(chart_map["Revenue Distribution"], width=260, height=160))
    flow.append(Spacer(1, 20))

    # -------------------------------------------------------------------------
    # REFERENCE TABLES
    # -------------------------------------------------------------------------
    flow.append(Spacer(1, 20))
    flow.append(Paragraph("Reference Data Tables", styles["SecHeader"]))
    flow.append(Spacer(1, 10))

    for title, df in dfs.items():
        flow.append(Paragraph(f"<b>{title}</b>", styles["ChartHeader"]))

        data = [df.columns.tolist()] + df.values.tolist()
        table = Table(data, repeatRows=1)

        table.setStyle(TableStyle([
            ("GRID", (0,0), (-1,-1), 0.4, colors.grey),
            ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ]))

        flow.append(table)
        flow.append(Spacer(1, 15))

    doc.build(flow)
