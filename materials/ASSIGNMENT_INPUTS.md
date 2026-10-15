# 作業識別與使用者提供材料（Kaggle S4E5 洪水預測升級版）

- 學號：`7115056106`
- 主程式名稱：`7115056106_hw2.py`
- 資料集：Kaggle Playground Series Season 4 Episode 5 (Regression with a Flood Prediction Dataset)
- 原始抽樣資料路徑：`data/raw/train.csv` (50,000 筆，20 個環境/工程輸入特徵，目標 `FloodProbability`，排除 `id`)

---

## 1. GPT 完整對話紀錄 PDF

- 原始檔案路徑：`/Users/esleyw/Desktop/洪水回歸題目選擇.pdf`
- 線上對話串 URL：https://chatgpt.com/c/6ad07fbb-127c-83e8-813d-1c9abb4c2e73
- 產生時間：2026/10/15 下午 3:35
- 對話主題：包含從作業目標、Kaggle 14–20 特徵篩選、選定 Predict the Flood 資料集、CRISP-DM 六階段完整架構、20 特徵回歸方程、RFE/Lasso 特徵選擇設計、95% 預測區間公式到完整執行 Prompt 的全過程紀錄。
- PDF 檔案大小：562,886 bytes
- 總頁數：**15 頁**
- PDF SHA-256：`830ffe1e70f743a7866dd4fdcea4b16c7a5f837029a46ce04700292602fb6c79`
- 存放位置：`materials/7115056106_GPT_conversation.pdf` 與 `submission/7115056106_hw2/7115056106_GPT_conversation.pdf`

---

## 2. NotebookLM 研究匯出 PDF

- 原始檔案路徑：`/Users/esleyw/Desktop/非引數貝氏Lasso與變數選擇 - Gemini Notebook.pdf`
- 線上筆記本 URL：https://notebook.google.com/notebook/59067a8c-667d-46d7-b9bc-3c71e19de5a4
- 產生時間：2026/10/15 下午 3:32
- 筆記本主題：非引數貝氏Lasso與變數選擇（涵蓋 10 個水文回歸與變數選擇學術來源）
- 摘要保存位置：`materials/NOTEBOOKLM_FLOOD_RESEARCH.md` 與 `submission/7115056106_hw2/NotebookLM_research_summary.md`
- PDF 檔案大小：236,966 bytes
- 總頁數：**2 頁**（完整排版未截斷版本，涵蓋三大模型優缺點、20 特徵 Lasso 限制與殘差診斷）
- PDF SHA-256：`08159842fea5317c85942902be79c0a7121c6d70120716884e5c3ec46cec42f5`
- 存放位置：`materials/7115056106_NotebookLM_export.pdf` 與 `submission/7115056106_hw2/7115056106_NotebookLM_export.pdf`

---

## 3. 打包與報告合併狀態

- **獨立主報告**：`report/7115056106_hw2_report.pdf`（12 頁），完整落實 CRISP-DM 六大階段與真實 NotebookLM 洪水研究摘要。
- **合併繳交報告**：`report/7115056106_hw2_report_with_appendix.pdf`（共 27 頁 = 12 頁主報告 + 15 頁真實 GPT 對話附錄）。
- **舊版紅酒除役聲明**：舊版 Red Wine Quality（11 特徵）之所有舊檔案、舊研究摘要與舊附件已全數清理移除，避免任何混淆。
