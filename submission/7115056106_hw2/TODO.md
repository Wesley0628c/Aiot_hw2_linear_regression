# HW2 多元線性回歸作業待辦清單（規格升級與改進版）

## 尚待使用者提供之核心材料（必備要求）

- [x] **提供符合 14–20 個特徵之 Kaggle 資料集原始檔**：
  - 已完成：使用者授權 Kaggle API Token，自動下載 Kaggle Playground Series S4E5（Flood Prediction）官方競賽資料集，並抽取 50,000 筆具統計代表性之樣本（`random_state=42`）存於 `data/raw/train.csv`（2.5 MB），包含 20 個環境/工程數值特徵，Target 為 `FloodProbability`，排除 `id`。
- [ ] **提供洪水主題之真實 NotebookLM 研究摘要與匯出 PDF**（作業核心必要項目）：
  - 要求：依課程規範，須使用 NotebookLM 研究同主題（洪水預測/水文環境回歸）解法，撰寫**至少 100 字摘要**並列出參考來源放入報告中；匯出真實 PDF 作為研究證據，取代舊版紅酒 PDF。
  - 目前狀態：已提供操作題綱於 `materials/FLOOD_NOTEBOOKLM_GUIDE.md`；待使用者於 NotebookLM 操作後提供文字摘要與匯出 PDF。
- [ ] **提供包含本次洪水版完整設計與修改歷程之 GPT 對話紀錄 PDF**（作業核心必要項目）：
  - 要求：原作業要求「所有與 ChatGPT 的對話匯出 PDF」。目前既有附件為舊版 22 頁紅酒對話，需補上/合併本次更換為 Kaggle S4E5 洪水資料集之規格討論、演算法管線修改、殘差診斷與驗收之完整對話 PDF。
  - 目前狀態：待使用者匯出包含新版歷程之對話 PDF。

---

## 執行與改進步驟

- [x] **Step 1A：資料規格查核與候選資料集驗證**  
  完成條件：確認原 11 特徵紅酒資料不符 14–20 特徵新規。完成 Kaggle Playground S4E5 欄位、Target、ID 與特徵數量驗證（20 特徵，符合 13 < features < 40 與 10–20 原始特徵規範）；盤點取得路徑並明確列出所需提供檔案。
- [x] **Step 1B：資料置換與路徑更新**  
  完成條件：取得 Kaggle S4E5 官方資料後，將抽樣驗證檔案置入 `data/raw/train.csv`，更新 `data/README.md` 與 `data/PREPARATION.md` 資料來源文檔與研究問題，避免混用舊版結果。
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
  - 使用 `pypdf` 及 `mdls` 實際解析附件 PDF 總頁數，更新 GPT 對話為 22 頁並附更正註記。
- [x] **Step 5A：跨平台報告生成器與雙版本 PDF 產出機制**  
  完成條件：
  - 移除 `report/generate_report.py` 單一 macOS 字型絕對路徑依賴，建立跨平台（macOS/Linux/Windows）字型解析與 `REPORT_FONT_PATH` 環境變數自訂機制。
  - 修正鏈結解析防雙重包裝問題，整合 `pypdf` 實現獨立主報告與主報告＋GPT 對話附錄合併 PDF 自動雙軌產出。
- [ ] **Step 5B：新資料 CRISP-DM 報告整合真實 NotebookLM 研究與對話附件**  
  完成條件：CRISP-DM 6 階段架構、模型指標與圖表已就緒；待使用者提供真實洪水主題 NotebookLM 100 字以上摘要與新版完整對話 PDF，將其正式整合入 `report/7115056106_hw2_report.md`、替換附件並重新編譯雙版本 PDF。
- [ ] **Step 6：打包最終繳交 ZIP 與乾淨環境重跑驗收**  
  完成條件：在 Step 5B 取得真實附件並重新編譯後，同步更新 `submission/7115056106_hw2/` 與 `submission/7115056106_hw2.zip`；解壓至獨立暫存目錄在無既有 outputs 下進行最終驗收重跑，確保檔案與數值 100% 正確。
