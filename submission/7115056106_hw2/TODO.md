# HW2 多元線性回歸作業待辦清單（規格升級與改進版）

## 使用者提供之核心材料驗收狀態

- [x] **提供符合 14–20 個特徵之 Kaggle 資料集原始檔**：
  - 已完成：使用者授權 Kaggle API Token，自動下載 Kaggle Playground Series S4E5（Flood Prediction）官方競賽資料集，並抽取 50,000 筆具統計代表性之樣本（`random_state=42`）存於 `data/raw/train.csv`（2.5 MB），包含 20 個環境/工程數值特徵，Target 為 `FloodProbability`，排除 `id`。
- [x] **提供洪水主題之真實 NotebookLM 研究摘要與匯出 PDF（保留原始檔與整理版）**：
  - 已完成：使用者於 Google NotebookLM 建立《非引數貝氏Lasso與變數選擇》筆記本，匯入 10 個水文與機器學習來源；保留 1 頁原始瀏覽器列印檔（`7115056106_NotebookLM_raw_export.pdf`，SHA-256：`f01a7c584e9229b52ee9453e14f4370f6c61e8c86f5ed64c45d956a9029680da`）；並如實排版產出 2 頁文獻整理版（`7115056106_NotebookLM_export.pdf`，SHA-256：`b8d0fd3a09d1c9f98001d77d0efb04b4e47304849bc4db655d2d28d77f735acc`），補入 Kaggle 官方優勝方案與真實學術文獻對照。
- [ ] **提供包含本次洪水版完整設計與修改歷程之 GPT 對話紀錄 PDF**：
  - **待完成（In Progress）**：目前已歸檔初期選題與 CRISP-DM 推導之 15 頁對話 PDF（`materials/7115056106_GPT_conversation.pdf`，URL：`https://chatgpt.com/c/6ad07fbb-127c-83e8-813d-1c9abb4c2e73`，SHA-256：`830ffe1e70f743a7866dd4fdcea4b16c7a5f837029a46ce04700292602fb6c79`）。後續程式碼修復、Jupyter 參數調校與 PDF 排版對話紀錄待完整補齊匯出後再正式標記驗收完成。

---

## 執行與改進步驟

- [x] **Step 1A：資料規格查核與候選資料集驗證**  
  完成條件：確認原 11 特徵紅酒資料不符 14–20 特徵新規。完成 Kaggle Playground S4E5 欄位、Target、ID 與特徵數量驗證（20 特徵，符合 13 < features < 40 與 10–20 原始特徵規範）；盤點取得路徑並明確列出所需提供檔案。
- [x] **Step 1B：資料置換與路徑更新**  
  完成條件：取得 Kaggle S4E5 官方資料後，將抽樣驗證檔案置入 `data/raw/train.csv`，更新 `data/README.md` 與 `data/PREPARATION.md` 資料來源文檔與研究問題，舊版紅酒檔案已徹底刪除清理。
- [x] **Step 2A：主程式動態標籤與通用架構改造**  
  完成條件：移除 `7115056106_hw2.py` 中寫死之「11 features」與「4 features」字串，改由模型摘要與實際篩選特徵動態生成；預留新欄位相容處理。
- [x] **Step 2B：新資料前處理、連續目標切分與基準/特徵選擇建模**  
  完成條件：針對連續目標實施 80/20 無資料洩漏切分（40,000 筆訓練、10,000 筆測試）；Pipeline 於 5-fold CV 內 fit `StandardScaler` 與 `Lasso`；訓練完整 20 特徵 OLS 基準模型與 1-SE 規則選定模型。
- [x] **Step 3：新模型評估、95% 預測區間與殘差診斷圖表**  
  完成條件：以同測試集產出 MAE (0.015814)、RMSE (0.020045)、R² (0.843482)、95% 個別新觀測預測區間（測試涵蓋率 94.28%、平均寬度 0.0785）及真實殘差診斷圖（DW=2.0047, JB p=0.0, BP p=0.0, Cook's D max=0.0027）。
- [x] **Step 4：校正統計數字、修正 Notebook、修正過度推論與文獻標註**  
  完成條件：
  - 依原始資料與 outputs 實際結果校正截距項為 -0.052739（約 -0.0527），校正目標偏態（0.0650）、目標峰度（Pearson 2.990，超額 -0.010）、特徵偏態（0.4072~0.4751）、特徵峰度（Pearson 3.124~3.405）、特徵間相關（-0.0232~+0.0042）與目標相關（0.1735~0.1942）。
  - 修復 `7115056106_hw2.ipynb`：移除系統帳號字串（改回 `id`）、補齊空白目標欄位（`FloodProbability`）、採用模組載入機制避免 `main()` 重複執行，並於主程式 `main(argv)` 改用 `parse_known_args()` 避免 Jupyter 參數衝突。
  - 修正過度推論：修正 Lasso「均等重要性」為合成資料對稱特徵訊號反映；修正 DW「證明獨立」為既定排序下一階序列相關檢定；修正高斯-馬可夫定理邊界（澄清定理保證 BLUE 不需常態性，常態性為精確預測區間之依據）；修正合成資料工程效益推論。
  - NotebookLM 如實標示為整理版，保留 1 頁原始瀏覽器列印檔，補入 Kaggle 官方優勝方案（aldparis 方案）與經典水文文獻對照。
  - GPT 對話完整性維持待完成狀態。
- [x] **Step 5：跨平台報告生成器與雙版本 PDF 重新產出**  
  完成條件：
  - 更新 `report/7115056106_hw2_report.md`，成功編譯 14 頁獨立主報告 `report/7115056106_hw2_report.pdf`。
  - 整合 14 頁主報告 + 15 頁 GPT 對話附錄 + 2 頁 NotebookLM 文獻整理附錄，成功產出 31 頁合併 PDF `report/7115056106_hw2_report_with_appendix.pdf`。
- [x] **Step 6：打包最終繳交 ZIP 與乾淨環境重跑驗收**  
  完成條件：同步 `submission/7115056106_hw2/` 全數更新檔，重新打包 `submission/7115056106_hw2.zip`，驗證解壓與重跑全數通過，雜湊與清單完全一致。
