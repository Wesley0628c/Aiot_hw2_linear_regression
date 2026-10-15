# AIoT HW2：Kaggle S4E5 洪水預測多元線性回歸分析 (Multiple Linear Regression)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.0%2B-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-Academic-lightgrey.svg)]()

> **學生學號**：7115056106  
> **作業主題**：以環境水文與防洪基礎設施特徵預測洪水機率（Flood Prediction Linear Regression Analysis）  
> **資料來源**：[Kaggle Playground Series s4e5](https://www.kaggle.com/competitions/playground-series-s4e5)  
> **特徵規格**：符合課程新修規範（14–20 個原始輸入特徵，滿足 $10 \le \text{features} \le 20$ 與 $13 < \text{features} < 40$ 雙重要求，排除 `id` 與目標恰為 20 個特徵）  
> **分析架構**：CRISP-DM 跨產業資料探勘標準流程

---

## 專案簡介 (Overview)

本專案使用 Kaggle 公開之 **Playground Series Season 4 Episode 5 (Regression with a Flood Prediction Dataset)**，針對區域環境水文、土地利用與防災基礎設施之 20 項連續評分特徵，透過標準 **CRISP-DM** 流程建立多元線性回歸模型，預測連續型洪水發生機率（`FloodProbability`）。

為兼顧計算效能、重複檢驗速度與版本庫大小限制，以固定隨機狀態（`random_state=42`）抽取 50,000 筆具統計代表性之樣本，經查核缺失值為 0 筆、特徵組合重複列為 0 筆。

專案落實嚴謹的統計機器學習實踐：
1. **防止 Data Leakage**：連續目標採用標準 80/20 獨立切分（40,000 筆訓練、10,000 筆測試），測試集從未參與特徵統計與模型訓練。
2. **正則化特徵選擇**：在 5-fold 交叉驗證內部以 Pipeline 封裝 `StandardScaler` 與 `Lasso`，採納 **One-Standard-Error (1-SE) 規則**搜尋最佳正則化強度 $\alpha \approx 0.000391$。實證顯示 20 項特徵均具備實質貢獻，保留完整 20 項特徵。
3. **推論診斷與區間估計**：提供 10,000 筆測試集個別新觀測之 **95% 預測區間（Individual Prediction Interval）**，並對殘差進行 Jarque-Bera（常態性）、Breusch-Pagan（等變異性）、Durbin-Watson（自相關性）與 Cook's Distance（影響點）嚴謹檢定。

---

## 核心實驗結果 (Key Results)

### 模型表現評估 (Test Set Performance)

| 模型名稱 | 輸入特徵數 | 測試集 MAE | 測試集 RMSE | 測試集 R² | 解釋變異量 |
|---|:---:|:---:|:---:|:---:|:---:|
| **基準模型 (Baseline OLS)** | 20 | **0.015814** | **0.020045** | **0.843482** | **84.35%** |
| **特徵選擇模型 (Selected OLS)** | 20 | **0.015814** | **0.020045** | **0.843482** | **84.35%** |

> **結論摘要**：20 項環境特徵能解釋超過 **84.35%** 的洪水機率變異。在 1-SE 規則下，Lasso 維持保留 20 項特徵，印證各項環境與工程指標在區域致災評估中的均衡重要性。

### 統計診斷與預測區間 (Diagnostics)

- **95% 個別預測區間涵蓋率**：10,000 筆未見測試集上達到 **94.28%**（名目值 95.0%），平均區間寬度約 **0.0785**（$\pm 3.9$ 個百分點）。
- **殘差假設檢定結果**：
  - **Durbin-Watson**：**2.004697**（接近 2.0，樣本獨立無一階自相關）。
  - **Jarque-Bera 檢定**：統計量 5653.83，$p = 0.000 < 0.05$（殘差呈現微幅偏態與高狹峰，拒絕常態性假設）。
  - **Breusch-Pagan 檢定**：LM 統計量 1701.03，$p = 0.000 < 0.05$（存在微幅異質變異，拒絕等變異假設）。
  - **Cook's Distance**：最大值僅 0.002688，遠小於 1.0，無破壞性影響點。
- **誠實揭露**：由於常態性與等變異性未完全成立，95% 預測區間應審慎視為高維線性投影下之優良近似。

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
│   │   └── train.csv            # Kaggle S4E5 洪水預測代表性抽樣資料集 (50,000 筆)
│   ├── processed/
│   │   ├── train.csv            # 劃分之獨立訓練集 (40,000 筆)
│   │   └── test.csv             # 劃分之獨立測試集 (10,000 筆)
│   ├── README.md                # 資料集欄位定義與來源說明
│   └── PREPARATION.md           # 資料前處理與切分邏輯規格書
├── materials/                   # 參考文獻、提示詞與輔助研究材料
│   ├── ASSIGNMENT_INPUTS.md     # 附件檔案來源與 SHA-256 紀錄
│   ├── NOTEBOOKLM_FLOOD_RESEARCH.md # NotebookLM 洪水預測深入研究摘要與解法比較
│   └── FLOOD_NOTEBOOKLM_GUIDE.md# S4E5 洪水預測 NotebookLM 研究與提問指引
├── outputs/                     # 程式產出之成果物 (可完全由主程式重現)
│   ├── figures/                 # 視覺化圖表 (熱力圖、殘差圖、預測區間圖等)
│   ├── tables/                  # 評估指標、特徵係數、描述統計等 CSV / JSON
│   └── models/                  # 序列化保存之模型 (Joblib)
├── report/                      # CRISP-DM 完整書面報告
│   ├── 7115056106_hw2_report.md # 報告 Markdown 原始檔
│   ├── 7115056106_hw2_report.pdf# 報告正式 PDF 檔案 (13 頁)
│   ├── 7115056106_hw2_report_with_appendix.pdf # 主報告結合 GPT 對話附錄之合併 PDF (28 頁)
│   └── generate_report.py       # 跨平台 PDF 報告編譯生成腳本
└── submission/                  # 作業正式打包壓縮檔與相關繳交附件
    ├── 7115056106_hw2.zip       # 最終作業壓縮檔
    └── 7115056106_hw2/          # 解壓對應之作業交付完整目錄
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

執行主程式將自動依序執行 CRISP-DM 六大階段，並在 `data/processed/` 與 `outputs/` 目錄中生成所有前處理資料、表格、圖表與模型：

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
本腳本支援跨平台 CJK 中文字型自動搜尋（macOS、Linux、Windows），並支援透過環境變數 `REPORT_FONT_PATH` 自訂字型路徑。

---

## 主要產出圖表說明 (Key Figures)

- **`outputs/figures/correlation_heatmap.png`**：20 項環境特徵與預測目標之相關矩陣熱力圖。
- **`outputs/figures/lasso_feature_selection.png`**：Lasso 特徵選擇之 CV RMSE 調校歷程與標準化迴歸係數收縮長條圖。
- **`outputs/figures/actual_vs_predicted.png`**：獨立測試集 10,000 筆真實值 vs 預測值對比散布圖（附理想預測 $y = \hat{y}$ 對角線）。
- **`outputs/figures/selected_model_95_prediction_intervals.png`**：精簡模型之個別觀測 95% 預測區間（Prediction Interval）覆蓋分布圖。
- **`outputs/figures/selected_model_residual_diagnostics.png`**：殘差分布直方圖、常態 Q-Q 圖、殘差 vs 擬合值散布圖與 Cook's 距離影響點診斷圖。

---

## 繳交附件聲明 (Submission Note)

本專案於 `submission/` 資料夾內包含符合課程繳交規格之 ZIP 檔案與相關 PDF 紀錄：
- `7115056106_hw2_report.pdf`：主研究報告（13 頁）
- `7115056106_hw2_report_with_appendix.pdf`：主報告結合 GPT 對話附錄之合併 PDF（28 頁）
- `7115056106_GPT_conversation.pdf`：作業輔助對話紀錄原始檔（15 頁）
- `7115056106_NotebookLM_export.pdf`：NotebookLM 研究紀錄原始檔（1 頁）
- SHA-256 校驗碼與來源對應詳見 [ASSIGNMENT_INPUTS.md](materials/ASSIGNMENT_INPUTS.md)。
