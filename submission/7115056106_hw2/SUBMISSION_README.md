# 7115056106 HW2 繳交說明

## 必要檔案

- `7115056106_hw2.py`：主程式。
- `7115056106_hw2_report.pdf`：CRISP-DM 主報告。
- `7115056106_GPT_conversation.pdf`：使用者匯出的真實 GPT 對話紀錄。
- `7115056106_NotebookLM_export.pdf`：使用者匯出的 NotebookLM 研究紀錄。
- `NotebookLM_research_summary.md`：經來源查核的 NotebookLM 摘要與解法比較。
- `data/raw/winequality-red.csv`：Kaggle Red Wine Quality 原始資料。
- `requirements.txt`：Python 套件版本。

`data/processed/` 與 `outputs/` 是實際執行結果，供核對報告數值及圖表；主程式可重新產生這些內容。

## 執行方式

在本資料夾根目錄執行：

```bash
MPLCONFIGDIR=/tmp/aiot_hw2_matplotlib \
PYTHONPYCACHEPREFIX=/tmp/aiot_hw2_pycache \
python3 7115056106_hw2.py
```

預設輸入為 `data/raw/winequality-red.csv`，處理後資料寫入 `data/processed/`，表格、模型及圖片寫入 `outputs/`。

## 重要分析設定

- 固定亂數種子：42。
- 完全相同的 11 個特徵及 `quality` 視為同組，避免跨越訓練／測試集合。
- Lasso 的標準化位於 Pipeline，僅在訓練 fold 內 fit。
- 預測區間為精簡 OLS 對個別未來觀測建立的 95% prediction interval。

## 附件來源聲明

兩份附件 PDF 均由使用者實際提供；本專案只重新命名並納入 ZIP，未虛構或改寫其內容。原始路徑與 SHA-256 紀錄見 `materials/ASSIGNMENT_INPUTS.md`。
