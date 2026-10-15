# 7115056106 HW2 繳交說明

## 必要檔案清單

- `7115056106_hw2.py`：主分析程式（涵蓋 CRISP-DM 探索、切分、Lasso 交叉驗證、模型擬合、預測區間與殘差檢定）。
- `7115056106_hw2.ipynb`：Jupyter Notebook 執行檔（已修復參數衝突、重複執行與欄位標記）。
- `7115056106_hw2_report.pdf`：CRISP-DM 正式主報告（14 頁）。
- `7115056106_hw2_report_with_appendix.pdf`：主報告結合 GPT 對話附錄與文獻整理之合併 PDF（31 頁）。
- `7115056106_GPT_conversation.pdf`：階段性真實 GPT 對話紀錄（15 頁，後續程式修復對話待補齊，完整性維持待完成）。
- `7115056106_NotebookLM_raw_export.pdf`：NotebookLM 原始瀏覽器列印存檔（1 頁原始紀錄）。
- `7115056106_NotebookLM_export.pdf`：NotebookLM 文獻排版整理版（2 頁完整版，涵蓋 10 個水文與變數選擇來源、Kaggle 優勝方案）。
- `NotebookLM_research_summary.md`：真實 NotebookLM 洪水研究摘要與主流解法比較（超過 100 字）。
- `data/raw/train.csv`：Kaggle Playground S4E5 洪水預測原始抽樣資料（50,000 筆，20 個原始特徵）。
- `requirements.txt`：Python 執行環境套件相依清單。

`data/processed/` 與 `outputs/` 為腳本執行後產生之實際結果，供核對報告數值及圖表；主程式可在無快取狀態下完全自主重新產生這些內容。

## 執行與重現方式

在本資料夾根目錄執行：

```bash
MPLCONFIGDIR=/tmp/aiot_hw2_matplotlib \
PYTHONPYCACHEPREFIX=/tmp/aiot_hw2_pycache \
python3 7115056106_hw2.py
```

預設輸入為 `data/raw/train.csv`，處理後訓練集與測試集寫入 `data/processed/`，所有評估表格、模型檔及圖片寫入 `outputs/`。

重新編譯 PDF 報告指令：
```bash
python3 report/generate_report.py
```

## 重要分析設定與規格核對

- **學號**：`7115056106`。
- **特徵數量**：恰為 20 個原始特徵（MonsoonIntensity 至 PoliticalFactors），符合課程 14–20 特徵新規。
- **目標變數**：`FloodProbability`（連續機率值，排除 `id`）。
- **資料切分**：80% 訓練集（40,000 筆）、20% 測試集（10,000 筆），固定亂數種子 `random_state=42`。
- **防洩漏設定**：Lasso 特徵選擇之 `StandardScaler` 位於 Pipeline 中，僅在 5-fold CV 訓練子集內 fit。
- **預測區間**：針對個別未來觀測建立之 95% Individual Prediction Interval（測試集涵蓋率 94.28%）。
- **截距項與斜率**：基準模型與特徵選擇模型截距項約為 -0.0527，未標準化特徵斜率集中於 0.00555 至 0.00574 之間。

## 附件來源聲明

所有附件 PDF 與來源檔案均由使用者實際提供或由程式真實編譯生成，無虛構造假。原始路徑與 SHA-256 驗證碼詳見 `materials/ASSIGNMENT_INPUTS.md`。
