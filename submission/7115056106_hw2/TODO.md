# HW2 多元線性回歸作業待辦清單（規格升級與改進版）

## 尚待使用者確認／提供

- [ ] **提供符合 14–20 個特徵之 Kaggle 資料集原始檔**：
  - 首選建議：Kaggle Playground Series S4E5（Flood Prediction）之 `train.csv`（或 10,000–50,000 筆隨機抽樣版本，以兼顧執行速度與 GitHub 檔案限制）。
  - 目標特徵：20 個環境/工程數值特徵，Target 為 `FloodProbability`，排除 `id`。
- [ ] **提供更換資料集後之真實 GPT 對話紀錄 PDF**（若更換資料集）。
- [ ] **提供更換資料集後之真實 NotebookLM 研究摘要與匯出 PDF**（若更換資料集；指引見 `materials/FLOOD_NOTEBOOKLM_GUIDE.md`）。

---

## 執行與改進步驟

- [x] **Step 1A：資料規格查核與候選資料集驗證**  
  完成條件：確認原 11 特徵紅酒資料不符 14–20 特徵新規。完成 Kaggle Playground S4E5 欄位、Target、ID 與特徵數量驗證（20 特徵，符合 13 < features < 40 與 10–20 原始特徵規範）；盤點取得路徑並明確列出所需提供檔案。
- [ ] **Step 1B：資料置換與路徑更新**  
  完成條件：在取得使用者提供之真實新資料集後，將檔案置入 `data/raw/`，更新資料來源文檔與研究問題，避免混用舊版結果。
- [x] **Step 2A：主程式動態標籤與通用架構改造**  
  完成條件：移除 `7115056106_hw2.py` 中寫死之「11 features」與「4 features」字串，改由模型摘要與實際篩選特徵動態生成；預留新欄位相容處理。
- [ ] **Step 2B：新資料前處理、連續目標切分與基準/特徵選擇建模**  
  完成條件：針對連續目標實施無資料洩漏切分；Pipeline 於 CV fold 內 fit；訓練完整特徵 OLS 基準模型與 Lasso 精簡 OLS。
- [ ] **Step 3：新模型評估、95% 預測區間與殘差診斷圖表**  
  完成條件：以同測試集產出 MAE、RMSE、R²、95% prediction interval（含涵蓋率與寬度）及真實殘差診斷圖。
- [x] **Step 4：修正文件一致性與歷史紀錄校正**  
  完成條件：
  - 修正 README 中 Durbin-Watson 為實際值 1.688651，且避免僅憑接近 2 宣稱無自相關。
  - 修正 README 中 `train.csv` 不含 `group_id` 之描述。
  - 修正 README 中 Lasso 圖為「Lasso 標準化迴歸係數長條圖」。
  - 修正 README 中所有 `file:///Users/...` 絕對連結為相對連結。
  - 修正 `materials/ASSIGNMENT_INPUTS.md` 附件「尚未打包」過期狀態。
  - 使用 `pypdf` 及 `mdls` 實際解析附件 PDF 總頁數，更新 GPT 對話為 22 頁（非 8 頁）並附更正註記。
- [x] **Step 5A：跨平台報告生成器與雙版本 PDF 產出**  
  完成條件：
  - 移除 `report/generate_report.py` 單一 macOS 字型絕對路徑依賴，建立跨平台（macOS/Linux/Windows）字型解析與 `REPORT_FONT_PATH` 環境變數自訂機制。
  - 整合 `pypdf` 實現獨立主報告（12 頁）與主報告＋GPT 對話附錄合併 PDF（34 頁）自動雙軌產出。
- [ ] **Step 5B：新資料 CRISP-DM 報告與 NotebookLM 研究整合**  
  完成條件：以新資料重構 6 階段報告；整合真實新主題 NotebookLM 摘要與文獻比較；標示 GPT 輔助內容。
- [ ] **Step 6：打包最終繳交 ZIP 與乾淨環境重跑驗收**  
  完成條件：建立 `submission/7115056106_hw2.zip`；解壓至獨立暫存目錄在無既有 outputs 下重跑通過並驗證數值一致。
