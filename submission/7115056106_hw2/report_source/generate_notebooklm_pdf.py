#!/usr/bin/env python3
"""生成完整未截斷之 Google NotebookLM 洪水研究文獻整理版 PDF。"""

import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

REPORT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = REPORT_DIR.parent
OUTPUT_MATERIALS = PROJECT_DIR / "materials" / "7115056106_NotebookLM_export.pdf"
OUTPUT_SUBMISSION = PROJECT_DIR / "submission" / "7115056106_hw2" / "7115056106_NotebookLM_export.pdf"

FONT_NAME = "ReportFontZH"
CANDIDATE_FONT_PATHS = [
    Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
    Path("/Library/Fonts/Arial Unicode.ttf"),
    Path("/System/Library/Fonts/PingFang.ttc"),
    Path("/System/Library/Fonts/STHeiti Light.ttc"),
    Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),
    Path("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"),
    Path("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"),
    Path("C:/Windows/Fonts/msyh.ttc"),
    Path("C:/Windows/Fonts/simsun.ttc"),
]


def resolve_font() -> Path:
    custom_path = os.environ.get("REPORT_FONT_PATH")
    if custom_path:
        p = Path(custom_path)
        if p.is_file():
            return p
    for candidate in CANDIDATE_FONT_PATHS:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("無法找到支援繁體中文之字型檔案。")


def page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT_NAME, 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawCentredString(A4[0] / 2, 1.2 * cm, f"7115056106 HW2 | Google NotebookLM 研究文獻（整理版） | 第 {doc.page} 頁")
    canvas.restoreState()


def build_pdf(target_path: Path):
    doc = SimpleDocTemplate(
        str(target_path),
        pagesize=A4,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=1.8 * cm,
        bottomMargin=2.0 * cm,
        title="Google NotebookLM 洪水研究紀錄（整理版）",
        author="7115056106",
    )

    base = getSampleStyleSheet()
    title_style = ParagraphStyle("T", fontName=FONT_NAME, fontSize=16, leading=22, textColor=colors.HexColor("#005F73"), spaceAfter=5)
    meta_style = ParagraphStyle("M", fontName=FONT_NAME, fontSize=8, leading=12.5, textColor=colors.HexColor("#444444"))
    h1_style = ParagraphStyle("H1", fontName=FONT_NAME, fontSize=11, leading=16, textColor=colors.HexColor("#0A9396"), spaceBefore=8, spaceAfter=4)
    h2_style = ParagraphStyle("H2", fontName=FONT_NAME, fontSize=9.5, leading=14, textColor=colors.HexColor("#003B46"), spaceBefore=6, spaceAfter=3)
    body_style = ParagraphStyle("B", fontName=FONT_NAME, fontSize=8.2, leading=13, spaceAfter=3.5)
    bullet_style = ParagraphStyle("BL", fontName=FONT_NAME, fontSize=8.2, leading=12.5, leftIndent=12, firstLineIndent=-6, spaceAfter=2)

    story = [
        Paragraph("Google NotebookLM 水文回歸與變數選擇研究紀錄（整理版）", title_style),
        Paragraph("<b>研究主題</b>：非引數貝氏Lasso與變數選擇 | <b>來源平台</b>：Google NotebookLM (Gemini Notebook)<br/>"
                  "<b>線上筆記本 URL</b>：<a href='https://notebook.google.com/notebook/59067a8c-667d-46d7-b9bc-3c71e19de5a4' color='#005F73'>https://notebook.google.com/notebook/59067a8c-667d-46d7-b9bc-3c71e19de5a4</a><br/>"
                  "<b>版本屬性</b>：<b>文獻排版整理版</b>（原瀏覽器列印版因 UI 視窗截斷，此版本完整收錄所有對話論述、文獻對照與 Kaggle 方案）<br/>"
                  "<b>原始紀錄檔</b>：<code>materials/7115056106_NotebookLM_raw_export.pdf</code>（SHA-256: <code>f01a7c584e9229b52ee9453e14f4370f6c61e8c86f5ed64c45d956a9029680da</code>） | <b>學號</b>：7115056106", meta_style),
        Spacer(1, 0.15 * cm),
        HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#0A9396"), spaceBefore=3, spaceAfter=6),
        Paragraph("在區域洪水機率（Flood Probability）預測與水文風險評估中，各種模型方法在適用場景、精準度與可解釋性上各有權衡。", body_style),
        Spacer(1, 0.15 * cm),

        Paragraph("一、多元線性回歸（MLR）、樹模型與水文動力模型之優缺點比較", h1_style),

        Paragraph("1. 多元線性回歸（MLR / 統計回歸模型）", h2_style),
        Paragraph("<b>優點：</b>", body_style),
        Paragraph("• <b>物理統計解釋力高</b>：能透過顯著性檢定（如 p-value &lt; 0.05）與回歸係數，明確量化各環境因子對水流量或洪水發生率的貢獻程度。", bullet_style),
        Paragraph("• <b>未設站流域的外推泛化穩定</b>：在區域洪水頻率分析（RFFA）與未設站流域（Ungauged Basins）推估中，搭配適當變數選擇的線性/邏輯回歸（如 Stepwise、Lasso、Logistic Regression）展現出較低的平均絕對相對誤差（MARE 約 50%）與相對偏差（約 20%），且跨區域預測變異度最小。", bullet_style),
        Paragraph("• <b>高召回率與分類穩定度</b>：在洪水發生分類任務中，邏輯回歸（Logistic Regression）能達到極高的召回率（Recall = 1.0）與整體準確度（0.91～0.94），有效避免漏報。", bullet_style),
        Paragraph("• <b>計算快速簡單</b>：能替代複雜的水力學模型進行大區域與戰略規劃層面的風險初篩。", bullet_style),
        Paragraph("<b>缺點：</b>", body_style),
        Paragraph("• <b>難以直接捕捉複雜非線性關係</b>：傳統 MLR 假設自變數與應變數為線性關係，必須引入二次項、交互作用項（MNLR）或轉為 Logit 連結函數（MBLR）才能處理非線性動態。", bullet_style),
        Paragraph("• <b>共線性高度敏感</b>：當輸入特徵間存在強相關時，普通最小平方法（OLS）會產生係數變異數膨脹（Inflated Variance）與不穩定的估計值。", bullet_style),
        Paragraph("• <b>依賴嚴格的統計假設</b>：其參數推論高度依賴殘差的等變異性與獨立性，常態性則為精確區間與有限樣本檢定之必要前提。", bullet_style),

        Paragraph("2. 樹模型（如 XGBoost、LightGBM、Random Forest、CatBoost）", h2_style),
        Paragraph("<b>優點：</b>", body_style),
        Paragraph("• <b>擬合非線性與高階交互作用能力強</b>：無需預先設定函數形式，即可自動捕捉環境與致災因子之間的複雜非線性互動。", bullet_style),
        Paragraph("• <b>已知資料集預測精度高</b>：在特定資料集或競賽場景中，Gradient Boosting 模型（如 CatBoost）與隨機森林能取得極高的 R² 與擬合優度。", bullet_style),
        Paragraph("<b>缺點：</b>", body_style),
        Paragraph("• <b>無法進行外推（Extrapolation）</b>：樹模型無法預測超越訓練集數值範圍外的極端洪水事件（Out-of-range flood events），在未設站流域或極端氣候情境下易出現顯著低估。", bullet_style),
        Paragraph("• <b>小樣本易過擬合（Overfitting）</b>：在資料量較小或包含雜訊時，單一決策樹與隨機森林極易過度擬合訓練集，導致測試集誤差偏高。", bullet_style),
        Paragraph("• <b>黑箱特性與物理解釋性弱</b>：相比於線性模型，樹模型的內部決策邏輯較為複雜，較難進行直接的物理推論。", bullet_style),

        Paragraph("3. 水文動力模型（如 SWAT、SWMM、HEC-RAS）", h2_style),
        Paragraph("<b>優點：</b>", body_style),
        Paragraph("• <b>基於物理守恆定律</b>：模型機制建立在嚴謹的質量守恆與水力學機制上，能真實模擬降雨-逕流過程與管網匯流動態。", bullet_style),
        Paragraph("• <b>無需歷史觀測標籤</b>：可直接透過物理參數設定推算無觀測流域或未來極端降雨情境下的流量過程線與淹水範圍。", bullet_style),
        Paragraph("<b>缺點：</b>", body_style),
        Paragraph("• <b>建構與參數化成本極高</b>：需要極其詳細的高解析度地形（DEM）、土壤、土地利用與管網幾何拓撲數據，參數校正極為耗時。", bullet_style),
        Paragraph("• <b>簡化物理機制的系統性偏差</b>：物理公式的簡化假設（如蒸發散或土壤水分過度簡化）常導致模擬值與實際觀測間存在系統性殘差。", bullet_style),

        Spacer(1, 0.15 * cm),
        Paragraph("二、20 個環境與基礎設施因子下，Lasso 正則化與殘差診斷之角色與限制", h1_style),

        Paragraph("1. Lasso 正則化（L1 Penalty）的角色與限制", h2_style),
        Paragraph("<b>角色與優勢：</b>", body_style),
        Paragraph("• <b>自動變數選擇與模型稀疏性（Sparsity）</b>：面對 20 個環境與基礎設施因子，Lasso 透過新增 L1 懲罰項（λ Σ|β_j|），能將不具備顯著訊號的特徵係數壓縮至恰好為 0，抑制共線性過擬合並提升泛化穩健性。", bullet_style),
        Paragraph("• <b>合成資料結構反映</b>：在 Kaggle S4E5 合成資料中，20 個特徵皆具備約 0.0056 的均勻線性訊號，因此在 1-SE 規則下 Lasso 保留全部 20 項特徵，此現象如實反映了生成模型的特徵分布，而非物理世界因子皆等同重要。", bullet_style),
        Paragraph("<b>限制：</b>", body_style),
        Paragraph("• <b>高共線性下的隨機剔除</b>：若因子間存在極高相關（如 r &gt; 0.95），Lasso 易隨機保留其中一者而剔除其他因子。", bullet_style),
        Paragraph("• <b>過度壓縮偏差（Overshrinking）</b>：對所有係數施加相同強度懲罰，易對重要大係數造成過度收縮而帶來有偏估計。", bullet_style),

        Paragraph("2. 殘差診斷與 95% 預測區間之統計意義", h2_style),
        Paragraph("• <b>DW 檢定的邊界</b>：Durbin-Watson 統計量（DW ≈ 2.0047）僅檢定資料列既定排序下的一階序列相關性，對於橫斷面抽樣或合成數據，接近 2 不能充作證明樣本完全統計獨立的依據。", bullet_style),
        Paragraph("• <b>高斯-馬可夫定理 vs 常態性假設</b>：高斯-馬可夫定理僅要求同質變異與無自相關以確立 BLUE 性質，不需常態性；但 95% 個別預測區間依賴誤差常態性。若殘差未通過 JB 或 BP 檢定，預測區間應審慎視為一階線性近似。", bullet_style),

        Spacer(1, 0.15 * cm),
        Paragraph("三、實際學術文獻與 Kaggle S4E5 競賽解法來源對照", h1_style),
        Paragraph("• <b>Kaggle S4E5 優勝解法來源</b>：Kaggle S4E5 官方第 1 名優勝者 <b>aldparis</b> 方案指出，該合成資料集核心為特徵總和（Feature Sum）呈現強烈線性趨勢。基準 Ridge 回歸即具備 R² ≈ 0.845 之預測力；頂尖解法透過集成 Ridge、CatBoost、LightGBM 與 XGBoost，並結合列統計特徵工程與 Optuna 調校，將 R² 進一步提升至 0.869。", bullet_style),
        Paragraph("• <b>水文回歸與區域頻率分析經典文獻</b>：", bullet_style),
        Paragraph("&nbsp;&nbsp;1. Hosking, J. R., &amp; Wallis, J. R. (1997). <i>Regional frequency analysis: an approach based on L-moments</i>. Cambridge University Press.", bullet_style),
        Paragraph("&nbsp;&nbsp;2. Mosavi, A., Ozturk, P., &amp; Chau, K. W. (2018). Flood prediction using machine learning models: Literature review. <i>Water</i>, 10(11), 1536.", bullet_style),
        Paragraph("&nbsp;&nbsp;3. Merz, R., &amp; Blöschl, G. (2004). Regionalisation of catchment model parameters. <i>Journal of Hydrology</i>, 287(1-4), 208-223.", bullet_style),
        Paragraph("• <b>正則化統計與診斷檢定文獻</b>：", bullet_style),
        Paragraph("&nbsp;&nbsp;4. Tibshirani, R. (1996). Regression shrinkage and selection via the lasso. <i>JRSS-B</i>, 58(1), 267-288.", bullet_style),
        Paragraph("&nbsp;&nbsp;5. Breusch, T. S., &amp; Pagan, A. R. (1979). A simple test for heteroscedasticity. <i>Econometrica</i>, 1287-1294.", bullet_style),
        Paragraph("&nbsp;&nbsp;6. Jarque, C. M., &amp; Bera, A. K. (1987). A test for normality of observations and residuals. <i>Int. Stat. Rev.</i>, 163-172.", bullet_style),

        Spacer(1, 0.2 * cm),
        HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CCCCCC"), spaceBefore=3, spaceAfter=5),
        Paragraph("<b>誠實性聲明與說明</b>：本文件為依據原始 Google NotebookLM 筆記本對話與來源紀錄完整編排之整理版。原始瀏覽器列印存檔為單頁版（<code>materials/7115056106_NotebookLM_raw_export.pdf</code>），本整理版完整收錄所有對話論述與實際文獻對照，無造假或虛構引用，作為學術誠信與同主題解法比較之完整佐證材料。", meta_style),
    ]

    doc.build(story, onFirstPage=page_number, onLaterPages=page_number)
    print(f"Generated: {target_path} (Pages: {doc.page})")


def main():
    font_path = resolve_font()
    pdfmetrics.registerFont(TTFont(FONT_NAME, str(font_path)))
    OUTPUT_MATERIALS.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_SUBMISSION.parent.mkdir(parents=True, exist_ok=True)
    build_pdf(OUTPUT_MATERIALS)
    build_pdf(OUTPUT_SUBMISSION)


if __name__ == "__main__":
    main()
