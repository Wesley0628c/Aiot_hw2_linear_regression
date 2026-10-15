"""將 HW2 Markdown 報告轉成支援繁體中文及圖片的 PDF。"""

from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


REPORT_DIR = Path(__file__).resolve().parent
SOURCE = REPORT_DIR / "7115056106_hw2_report.md"
OUTPUT = REPORT_DIR / "7115056106_hw2_report.pdf"
FONT_PATH = Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf")
FONT_NAME = "ArialUnicode"


def inline_markup(text: str) -> str:
    value = html.escape(text.strip())
    value = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"\[([^]]+)\]\((https?://[^)]+)\)", r"<a href='\2' color='#005F73'>\1</a>", value)
    value = re.sub(r"(https?://[^\s<]+)", r"<a href='\1' color='#005F73'>\1</a>", value)
    return value


def page_number(canvas, document) -> None:
    canvas.saveState()
    canvas.setFont(FONT_NAME, 8)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawCentredString(A4[0] / 2, 1.1 * cm, f"7115056106 HW2  |  {document.page}")
    canvas.restoreState()


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("TitleZH", parent=base["Title"], fontName=FONT_NAME, fontSize=23, leading=31, textColor=colors.HexColor("#7F1D1D"), alignment=TA_CENTER, spaceAfter=14),
        "h1": ParagraphStyle("H1ZH", parent=base["Heading1"], fontName=FONT_NAME, fontSize=17, leading=23, textColor=colors.HexColor("#7F1D1D"), spaceBefore=12, spaceAfter=8),
        "h2": ParagraphStyle("H2ZH", parent=base["Heading2"], fontName=FONT_NAME, fontSize=13, leading=18, textColor=colors.HexColor("#005F73"), spaceBefore=9, spaceAfter=5),
        "body": ParagraphStyle("BodyZH", parent=base["BodyText"], fontName=FONT_NAME, fontSize=9.5, leading=15, alignment=TA_LEFT, spaceAfter=6),
        "bullet": ParagraphStyle("BulletZH", parent=base["BodyText"], fontName=FONT_NAME, fontSize=9.3, leading=14, leftIndent=14, firstLineIndent=-7, spaceAfter=3),
        "caption": ParagraphStyle("CaptionZH", parent=base["BodyText"], fontName=FONT_NAME, fontSize=8.5, leading=12, alignment=TA_CENTER, textColor=colors.HexColor("#555555"), spaceAfter=8),
        "code": ParagraphStyle("CodeZH", parent=base["Code"], fontName="Courier", fontSize=7.5, leading=10, leftIndent=10, backColor=colors.HexColor("#F3F4F6"), borderPadding=6, spaceAfter=8),
        "table": ParagraphStyle("TableZH", parent=base["BodyText"], fontName=FONT_NAME, fontSize=7.5, leading=10),
    }


def markdown_table(lines: list[str], style: ParagraphStyle) -> Table:
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append([Paragraph(inline_markup(cell), style) for cell in cells])
    column_count = max(len(row) for row in rows)
    available = A4[0] - 3.4 * cm
    table = Table(rows, colWidths=[available / column_count] * column_count, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6F2F2")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#003B46")),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#AAAAAA")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def build_story(markdown: str) -> list:
    style = styles()
    story = []
    lines = markdown.splitlines()
    index = 0
    first_heading = True
    while index < len(lines):
        line = lines[index].rstrip()
        if not line:
            index += 1
            continue
        if line == "<!-- pagebreak -->":
            story.append(PageBreak())
            index += 1
            continue
        if line.startswith("```"):
            code_lines = []
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                code_lines.append(lines[index])
                index += 1
            story.append(Paragraph("<br/>".join(html.escape(item) for item in code_lines), style["code"]))
            index += 1
            continue
        image_match = re.fullmatch(r"!\[([^]]*)\]\(([^)]+)\)", line)
        if image_match:
            caption, relative_path = image_match.groups()
            image_path = (REPORT_DIR / relative_path).resolve()
            image = Image(str(image_path))
            max_width, max_height = A4[0] - 3.4 * cm, 14.5 * cm
            scale = min(max_width / image.imageWidth, max_height / image.imageHeight, 1)
            image.drawWidth = image.imageWidth * scale
            image.drawHeight = image.imageHeight * scale
            story.append(KeepTogether([image, Paragraph(f"圖：{inline_markup(caption)}", style["caption"])]))
            index += 1
            continue
        if line.startswith("|"):
            table_lines = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index])
                index += 1
            story.append(markdown_table(table_lines, style["table"]))
            story.append(Spacer(1, 7))
            continue
        if line.startswith("# "):
            heading_style = style["title"] if first_heading else style["h1"]
            story.append(Paragraph(inline_markup(line[2:]), heading_style))
            first_heading = False
            index += 1
            continue
        if line.startswith("## "):
            story.append(Paragraph(inline_markup(line[3:]), style["h2"]))
            index += 1
            continue
        if re.match(r"^[-*] ", line):
            story.append(Paragraph("• " + inline_markup(line[2:]), style["bullet"]))
            index += 1
            continue
        number_match = re.match(r"^(\d+)\. (.+)", line)
        if number_match:
            story.append(Paragraph(f"{number_match.group(1)}. {inline_markup(number_match.group(2))}", style["bullet"]))
            index += 1
            continue
        paragraph_lines = [line]
        index += 1
        while index < len(lines) and lines[index].strip() and not re.match(
            r"^(#|[-*] |\d+\. |```|!\[|\||<!-- pagebreak)", lines[index].strip()
        ):
            paragraph_lines.append(lines[index].strip())
            index += 1
        story.append(Paragraph(inline_markup(" ".join(paragraph_lines)), style["body"]))
    return story


def main() -> None:
    if not FONT_PATH.is_file():
        raise FileNotFoundError(f"找不到中文字型：{FONT_PATH}")
    pdfmetrics.registerFont(TTFont(FONT_NAME, str(FONT_PATH)))
    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=1.7 * cm,
        leftMargin=1.7 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.8 * cm,
        title="HW2 多元線性回歸分析報告",
        author="7115056106",
        subject="Red Wine Quality CRISP-DM",
    )
    document.build(build_story(SOURCE.read_text(encoding="utf-8")), onFirstPage=page_number, onLaterPages=page_number)
    print(f"report_pdf={OUTPUT}")


if __name__ == "__main__":
    main()
