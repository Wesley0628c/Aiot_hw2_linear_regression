# AIoT HW2：Red Wine Quality 多元線性回歸分析 (Multiple Linear Regression)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.0%2B-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-Academic-lightgrey.svg)]()

> **學生學號**：7115056106  
> **作業主題**：以理化特徵預測紅酒感官品質（Red Wine Quality Linear Regression Analysis）  
> **分析架構**：CRISP-DM 跨產業資料探勘標準流程

---

## 專案簡介 (Overview)

本專案使用 Kaggle 公開之 [Red Wine Quality 資料集](https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009)（1,599 筆葡萄牙 Vinho Verde 紅酒樣本），透過 **CRISP-DM** 流程探討如何利用 11 項客觀理化檢驗數據建立多元線性回歸模型，輔助預測專家主觀感官品質評分（`quality`）。

專案特別針對資料集特性進行了嚴謹的統計檢定與機器學習工程處理：
1. **防範 Data Leakage**：識別出 240 筆完全重複樣本，採用**完全列群組分層抽樣（Stratified Group Split）**，確保相同理化樣本不會同時橫跨訓練集與測試集。
2. **嚴格特徵選擇**：在交叉驗證（CV）fold 內部實施標準化與 Lasso 特徵篩選，並採納 **One-Standard-Error (1-SE) 規則**挑選最精簡之特徵子集。
3. **完整統計檢定與區間估計**：提供個別未來觀測之 **95% 預測區間（Prediction Interval）**，並對殘差進行 Jarque-Bera（常態性）、Breusch-Pagan（等變異性）與 Durbin-Watson（自相關性）檢驗。

---

## 核心實驗結果 (Key Results)

### 模型表現評估 (Test Set Performance)

| 模型名稱 | 特徵數量 | MAE | RMSE | R² | 特徵精簡率 | RMSE 變化 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **基準模型 (Baseline OLS)** | 11 | **0.5032** | **0.6579** | **0.3418** |基準 | 基準 |
| **精簡模型 (Selected OLS)** | **4** | 0.5119 | 0.6641 | 0.3294 | **-63.64%** | +0.94% |

> **結論摘要**：精簡模型僅保留 4 項特徵（`alcohol`、`sulphates`、`volatile acidity`、`total sulfur dioxide`），特徵維度大幅縮減 **63.64%**，測試集 RMSE 僅微幅增加 **0.94%**，成功在模型可解釋性、資料採集成本與預測精度之間取得優異平衡。

### 統計診斷與預測區間 (Diagnostics)

- **95% 預測區間經驗涵蓋率**：測試集上達到 **94.64%**（理論值 95%）。
- **殘差診斷（舊版紅酒實測數據）**：
  - Durbin-Watson：實測統計量為 **1.688651**（依賴列排序，橫斷面資料無自然時間序列，不可僅憑數值接近 2 逕行宣稱無顯著自相關）。
  - Jarque-Bera 檢定：$p = 1.11 \times 10^{-8} < 0.05$（殘差非常態，未通過常態性假設）。
  - Breusch-Pagan 檢定：$p = 8.25 \times 10^{-6} < 0.05$（存在異質變異，未通過等變異假設）。

---

## 專案架構 (Project Structure)

```text
aiot_hw2_linear_regression/
├── 7115056106_hw2.py            # 主程式：資料載入、探索、模型訓練、評估與圖表產出
├── requirements.txt             # 執行環境相依套件清單
├── README.md                    # 專案完整說明文件
├── SUBMISSION_README.md         # 作業繳交必備規範與摘要說明
├── PROJECT_LOG.md               # 專案開發歷程與改動記錄
├── TODO.md                      # 開發任務追蹤清單
├── data/
│   ├── raw/
│   │   └── winequality-red.csv  # Kaggle 原始紅酒品質資料集 (舊版，待換 S4E5)
│   ├── processed/
│   │   ├── train.csv            # 劃分之獨立訓練集
│   │   └── test.csv             # 劃分之獨立測試集
│   ├── README.md                # 資料集欄位定義與來源說明
│   └── PREPARATION.md           # 資料前處理與切分邏輯規格書
├── materials/                   # 參考文獻、提示詞與輔助研究材料
│   ├── ASSIGNMENT_INPUTS.md
│   ├── NOTEBOOKLM_INPUT.md
│   └── NOTEBOOKLM_RESEARCH.md
├── outputs/                     # 程式產出之成果物 (可完全由主程式重現)
│   ├── figures/                 # 視覺化圖表 (熱力圖、殘差圖、預測區間圖等)
│   ├── tables/                  # 評估指標、特徵係數、描述統計等 CSV / JSON
│   └── models/                  # 序列化保存之模型 (Joblib)
├── report/                      # CRISP-DM 完整書面報告
│   ├── 7115056106_hw2_report.md # 報告 Markdown 原始檔
│   ├── 7115056106_hw2_report.pdf# 報告正式 PDF 檔案
│   └── generate_report.py       # PDF 報告生成腳本
└── submission/                  # 作業正式打包壓縮檔與相關繳交附件
    └── 7115056106_hw2.zip
```

---

## 安裝與環境需求 (Installation)

建議使用 Python 3.9 或以上版本。

1. **複製專案庫**：
   ```bash
   git clone https://github.com/Wesley0628c/Aiot_hw2_linear_regression.git
   cd Aiot_hw2_linear_regression
   ```

2. **建立並啟用虛擬環境（建議）**：
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # macOS / Linux
   # .venv\Scripts\activate   # Windows
   ```

3. **安裝依賴套件**：
   ```bash
   pip install -r requirements.txt
   ```

---

## 重現與執行方式 (Usage)

### 1. 執行主分析流程

執行主程式將依序完成 CRISP-DM 流程，並在 `data/processed/` 與 `outputs/` 目錄中生成所有預處理資料、表格、圖表與模型：

```bash
python3 7115056106_hw2.py
```

或使用自訂暫存隔離參數（避免系統快取干擾）：
```bash
MPLCONFIGDIR=/tmp/aiot_hw2_matplotlib \
PYTHONPYCACHEPREFIX=/tmp/aiot_hw2_pycache \
python3 7115056106_hw2.py
```

### 2. 重新產生 PDF 報告

若需要由 Markdown 重現編譯 PDF 報告：
```bash
python3 report/generate_report.py
```

---

## 主要產出圖表說明 (Key Figures)

- **`outputs/figures/correlation_heatmap.png`**：輸入特徵與預測目標之相關係數矩陣熱力圖。
- **`outputs/figures/lasso_feature_selection.png`**：Lasso 特徵選擇之標準化迴歸係數長條圖（依 1-SE 門檻篩選出非零入選特徵與歸零剔除特徵）。
- **`outputs/figures/actual_vs_predicted.png`**：獨立測試集真實值 vs 預測值對比散布圖（附理想預測 $y = \hat{y}$ 對角線）。
- **`outputs/figures/selected_model_95_prediction_intervals.png`**：精簡模型之個別觀測 95% 預測區間（Prediction Interval）覆蓋分布圖。
- **`outputs/figures/selected_model_residual_diagnostics.png`**：殘差分布直方圖、常態 Q-Q 圖、殘差 vs 擬合值等異質變異診斷圖。

---

## 繳交附件聲明 (Submission Note)

本專案於 `submission/` 資料夾內包含符合課程繳交規格之 ZIP 檔案與相關 PDF 紀錄：
- `7115056106_hw2_report.pdf`：主研究報告（12 頁）
- `7115056106_hw2_report_with_appendix.pdf`：主報告結合 GPT 對話附錄之合併 PDF（34 頁）
- `7115056106_GPT_conversation.pdf`：作業輔助對話紀錄原始檔（22 頁）
- `7115056106_NotebookLM_export.pdf`：NotebookLM 研究紀錄原始檔（3 頁）
- SHA-256 校驗碼與來源對應詳見 [ASSIGNMENT_INPUTS.md](materials/ASSIGNMENT_INPUTS.md)。
