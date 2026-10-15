# HW2 多元線性回歸作業待辦清單（規格升級與改進版）

## 使用者提供之核心材料（已全部驗收就緒）

- [x] **提供符合 14–20 個特徵之 Kaggle 資料集原始檔**：
  - 已完成：使用者授權 Kaggle API Token，自動下載 Kaggle Playground Series S4E5（Flood Prediction）官方競賽資料集，並抽取 50,000 筆具統計代表性之樣本（`random_state=42`）存於 `data/raw/train.csv`（2.5 MB），包含 20 個環境/工程數值特徵，Target 為 `FloodProbability`，排除 `id`。
- [x] **提供洪水主題之真實 NotebookLM 研究摘要與匯出 PDF**：
  - 已完成：使用者於 Google NotebookLM 建立《非引數貝氏Lasso與變數選擇》筆記本，匯入 10 個水文與機器學習來源；產出深具學術深度之 1000+ 字研究摘要（涵蓋 MLR、樹模型、水文動力模型優缺點、Lasso 稀疏性與過度壓縮限制、殘差診斷對 95% 預測區間影響）。匯出之 1 頁真實 PDF（`7115056106_NotebookLM_export.pdf`，SHA-256：`f01a7c584e9229b52ee9453e14f4370f6c61e8c86f5ed64c45d956a9029680da`）已正式歸檔至 `materials/` 與 `submission/7115056106_hw2/`。
- [x] **提供包含本次洪水版完整設計與修改歷程之 GPT 對話紀錄 PDF**：
  - 已完成：使用者提供《洪水回歸題目選擇.pdf》（15 頁，URL：`https://chatgpt.com/c/6ad07fbb-127c-83e8-813d-1c9abb4c2e73`，SHA-256：`830ffe1e70f743a7866dd4fdcea4b16c7a5f837029a46ce04700292602fb6c79`），完整記錄 14–20 特徵挑選、CRISP-DM 架構、RFE/Lasso 設計、95% 預測區間公式與執行 Prompt。已正式歸檔為 `7115056106_GPT_conversation.pdf`。

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
- [x] **Step 4：修正文件一致性與歷史紀錄校正**  
  完成條件：
  - 修正 README 中 Durbin-Watson 為實際值，且避免僅憑接近 2 宣稱無自相關。
  - 修正 README 中 `train.csv` 不含 `group_id` 之描述。
  - 修正 README 中 Lasso 圖為「Lasso 標準化迴歸係數長條圖」。
  - 修正 README 中所有 `file:///Users/...` 絕對連結為相對連結。
  - 修正 `materials/ASSIGNMENT_INPUTS.md` 附件「尚未打包」過期狀態。
  - 使用 `pypdf` 及 `mdls` 實際解析附件 PDF 總頁數，更新 GPT 對話為 15 頁並附更正註記。
- [x] **Step 5A：跨平台報告生成器與雙版本 PDF 產出機制**  
  完成條件：
  - 移除 `report/generate_report.py` 單一 macOS 字型絕對路徑依賴，建立跨平台（macOS/Linux/Windows）字型解析與 `REPORT_FONT_PATH` 環境變數自訂機制。
  - 修正鏈結解析防雙重包裝問題，整合 `pypdf` 實現獨立主報告與主報告＋GPT 對話附錄合併 PDF 自動雙軌產出。
- [x] **Step 5B：新資料 CRISP-DM 報告整合真實 NotebookLM 研究與對話附件**  
  完成條件：已將使用者提供之真實 NotebookLM 洪水研究摘要、方法比較表與 10 個來源完整整合入 `report/7115056106_hw2_report.md`，更新 GPT 協作宣告；成功編譯 13 頁獨立主報告 `report/7115056106_hw2_report.pdf` 與合併 15 頁真實 GPT 對話附錄之 28 頁合併 PDF `report/7115056106_hw2_report_with_appendix.pdf`。
- [x] **Step 6：打包最終繳交 ZIP 與乾淨環境重跑驗收**  
  完成條件：已同步 `submission/7115056106_hw2/` 並重新打包 `submission/7115056106_hw2.zip`（8.06 MB，`unzip -t` 59 個檔案完整無損）；解壓至 `/tmp/clean_hw2_final_test` 於無既有 outputs 與 processed 資料下執行主程式與報告生成器全數成功，數值 100% 重現一致。
