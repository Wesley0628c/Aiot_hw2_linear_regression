# HW2 多元線性回歸作業專案紀錄

## Step 0：檢查專案並建立管理檔

- 狀態：已完成
- 實際修改或完成項目：已檢查專案根目錄；檢查前未找到任何專案檔案，且此目錄不是 Git repository。建立 `TODO.md` 與 `PROJECT_LOG.md`，列入 Step 0–10、各步驗收條件與待使用者提供事項。
- 測試指令或方法：以 `test -s TODO.md && test -s PROJECT_LOG.md` 檢查兩檔存在且非空；以 `rg -c -- '- \\[x\\]' TODO.md` 檢查初始勾選狀態；以 `rg -c -- '\\*\\*Step [0-9]+[:：]' TODO.md` 計算步驟；以 `find . -maxdepth 1 -type f -print | sort` 盤點建立後檔案。
- 測試是否成功：成功。
- 實際輸出結果：管理檔測試輸出 `management_files=present_and_nonempty`；初始已勾選項目為 0（`rg` 無匹配）；步驟標題計數為 11（Step 0–10）；根目錄只列出 `PROJECT_LOG.md` 與 `TODO.md`。初始檢查亦顯示目前路徑為 `/Users/esleyw/Desktop/aiot_hw2_linear_regression`，當時 `find` 未列出檔案，且 `git status` 回傳 `fatal: not a git repository (or any of the parent directories): .git`。
- 產生或修改檔案：`TODO.md`、`PROJECT_LOG.md`。
- 尚未解決的問題或限制：無；Step 1 仍須由使用者確認資料集後才能完成。

## Step 1：選擇並確認資料集與研究問題

- 狀態：已完成
- 實際修改或完成項目：使用者已確認 Red Wine Quality。研究問題定為使用 11 個理化特徵預測 `quality`。已從 Kaggle 公開下載 API 取得 ZIP，檢查壓縮檔後解壓 `winequality-red.csv`，並建立資料來源紀錄。未開始資料探索或建模。
- 測試指令或方法：首次在 sandbox 執行 `curl`；因 DNS 限制失敗後，經核准以相同 Kaggle API 重新下載。使用 `file`、`unzip -l` 與 `shasum -a 256` 驗證壓縮檔；使用 Python 標準函式庫 `csv` 計算資料列、欄位、特徵數並檢查 `quality`。最後以 Python assertions 驗證 CSV 標題與預期 12 欄完全一致、資料列為 1,599、輸入特徵為 11、目標為 `quality`、SHA-256 與 Kaggle URL 均已寫入來源文件，且來源文件列出全部欄位。
- 測試是否成功：成功；最終輸出 `step1_validation=PASS`。
- 實際輸出結果：第一次下載錯誤為 `curl: (6) Could not resolve host: www.kaggle.com`；核准網路存取後成功下載 26,176 bytes。ZIP 內只有 `winequality-red.csv`（解壓大小 100,951 bytes）。CSV 實測 1,599 筆、12 欄、11 個輸入特徵，且 `target_present=True`。ZIP SHA-256 為 `f72e93e9670a3f7aefd38b318dea4a8e0534604cfe5088dab9a7bc1f991856a9`；CSV SHA-256 為 `d6a0d9bd24806944818795f22500c46cb6424cbff517aacda36595d3ed9b2daa`。
- 產生或修改檔案：`data/raw/winequality-red.csv`、`data/README.md`、`PROJECT_LOG.md`。
- 尚未解決的問題或限制：`quality` 是有序離散評分，線性回歸可能產生小數或超界預測；此限制須於 Evaluation 與報告討論，但不妨礙本作業以回歸方式建模。

## Step 2：Data Understanding

- 狀態：已完成
- 實際修改或完成項目：建立學號命名主程式，讀取並嚴格驗證 12 個預期欄位；輸出資料摘要、描述統計、各欄型態／缺失／唯一值、目標分布表，以及目標分布圖、Pearson 相關矩陣、11 個特徵直方圖。另登記使用者提供的學號、GPT PDF 與 NotebookLM 原文；NotebookLM 引用查核保留至 Step 7。
- 測試指令或方法：以 `MPLCONFIGDIR=/tmp/aiot_hw2_matplotlib python3 7115056106_hw2.py` 執行分析；用 assertions 驗證七個輸出均存在且非空、摘要數字、品質分布總數與主要類別筆數，並以 Pillow `Image.verify()` 驗證三張 PNG。第一次執行 `python3 -m py_compile` 因預設 bytecode 快取位於不可寫的使用者 Library 而失敗；改用 `PYTHONPYCACHEPREFIX=/tmp/aiot_hw2_pycache` 後編譯成功。另以全新 `/tmp/aiot_hw2_step2_verify` 輸出目錄重跑，對四份表格執行 `diff -u`，並目視檢查三張圖。
- 測試是否成功：最終成功。初次編譯測試失敗已記錄並修正；後續輸出 `compile=PASS`、`clean_rerun=PASS`、`table_reproducibility=PASS` 及 `step2_validation=PASS`。
- 實際輸出結果：1,599 筆、12 欄、11 個特徵；所有特徵為 `float64`，目標為 `int64`；缺失值 0；完全重複列 240。`quality` 範圍 3–8，平均 5.6360，中位數 6。品質分布為 3:10、4:53、5:681、6:638、7:199、8:18，明顯集中於 5 與 6。首次編譯錯誤為 `PermissionError: [Errno 1] Operation not permitted`（預設 Python cache 路徑），改用 `/tmp` cache 後通過。
- 產生或修改檔案：`7115056106_hw2.py`、`outputs/tables/data_summary.json`、`outputs/tables/descriptive_statistics.csv`、`outputs/tables/column_quality_summary.csv`、`outputs/tables/target_distribution.csv`、`outputs/figures/target_distribution.png`、`outputs/figures/correlation_heatmap.png`、`outputs/figures/feature_distributions.png`、`materials/ASSIGNMENT_INPUTS.md`、`materials/NOTEBOOKLM_INPUT.md`、`TODO.md`、`PROJECT_LOG.md`。
- 尚未解決的問題或限制：使用者已確認目前無法判定 240 筆完全重複列是不同酒樣的相同測量，或是重複匯入；Step 3 不直接刪除，而將完全相同列視為同組，確保同組只進入訓練集或測試集其中一邊，並清楚記錄此非逐列隨機抽樣的限制。多個特徵呈偏態且具有極端值，不能在未經診斷下任意刪除。品質 3、4、8 樣本少，分組切分時仍需盡量維持目標分布。

## Step 3：Data Preparation

- 狀態：已完成
- 實際修改或完成項目：保留全部 1,599 筆紀錄，使用 11 個特徵加 `quality` 的完整列定義群組；以固定 `random_state=42` 的 5-fold `StratifiedGroupKFold` 產生候選，選擇測試比例最接近 20% 且品質比例最接近全體的 fold。輸出 train/test CSV、切分摘要及準備決策文件。沒有缺失值需要插補、沒有類別特徵需要編碼；未任意刪除偏態或極端觀測，也未對全資料 fit 任何前處理器。
- 測試指令或方法：完整執行 `7115056106_hw2.py`；再以 `mktemp -d` 建立全新目錄重跑。用 Python assertions 與 `Counter` 驗證 train/test 合計 1,599 筆且每一完整列的出現次數與原始資料完全相同、兩集合的完整列集合不相交、缺失值皆為 0、品質 3–8 皆存在於兩集合、測試比例與 20% 相差小於 1 個百分點；逐 bytes 比較兩次執行的 train.csv、test.csv 與 split_summary.json。
- 測試是否成功：成功；輸出 `step3_validation=PASS`、`all_1599_rows_and_multiplicities_preserved=PASS`、`complete_row_overlap=0`、`reproducible_split=PASS`。
- 實際輸出結果：訓練集 1,282 筆、1,087 個群組；測試集 317 筆、272 個群組；測試比例 0.198249；群組交集 0；兩邊缺失值皆為 0。品質 3–8 均出現在兩邊。選用 fold 3。測試集品質計數為 3:2、4:16、5:132、6:129、7:35、8:3。
- 產生或修改檔案：`7115056106_hw2.py`、`data/processed/train.csv`、`data/processed/test.csv`、`data/PREPARATION.md`、`outputs/tables/split_summary.json`、`TODO.md`、`PROJECT_LOG.md`。
- 尚未解決的問題或限制：此方法不是逐列隨機抽樣；因群組大小不一，測試比例與各品質比例無法同時精確符合 20%／整體比例。品質 3、4、8 的測試樣本仍少，相關分數的誤差估計不穩定。若 Step 5 使用 Lasso 標準化，必須用 Pipeline 在各訓練 fold 內 fit，不能使用測試資料。

## Step 4：建立基準線性回歸模型

- 狀態：已完成
- 實際修改或完成項目：使用 Step 3 固定訓練集的全部 11 個特徵 fit `sklearn.linear_model.LinearRegression`（普通最小平方法、含截距）；對固定測試集產生逐筆預測與殘差，輸出 11 個係數、模型摘要及可重新載入的 joblib 模型。此步驟不把測試目標用於 fit，也不提前將 MAE、RMSE、R² 當作正式評估結果。
- 測試指令或方法：完整執行主程式並執行 `py_compile`；以新的暫存目錄重跑；重新載入 joblib 模型後對測試特徵預測，與 CSV 逐筆比較（絕對誤差容許 `1e-12`）；另外只用 train.csv 獨立 fit 新模型，比較係數與截距；驗證 317 筆預測均為有限數值且不為常數、實際值與 test.csv 相同、特徵順序為既定 11 欄；逐 bytes 比較兩次執行的預測、係數與摘要檔。
- 測試是否成功：成功；輸出 `step4_validation=PASS`、`saved_model_reload_predictions=PASS`、`independent_train_only_refit=PASS`、`reproducible_baseline_outputs=PASS`。
- 實際輸出結果：訓練 1,282 筆、預測 317 筆；11 個特徵；截距 25.9728853047；測試預測最小值 4.647604、最大值 7.505878、平均值 5.632106。正式誤差指標留待 Step 6 計算與解釋。
- 產生或修改檔案：`7115056106_hw2.py`、`outputs/tables/baseline_predictions.csv`、`outputs/tables/baseline_coefficients.csv`、`outputs/tables/baseline_model_summary.json`、`outputs/models/baseline_linear_regression.joblib`、`TODO.md`、`PROJECT_LOG.md`。
- 尚未解決的問題或限制：普通最小平方法係數受特徵量尺與共線性影響，不能直接用係數絕對值判定重要性；Step 5 將以只在訓練 fold fit 的標準化與特徵選擇處理。模型對離散品質分數輸出連續值，此限制於 Step 6 評估。

## Step 5：Feature Selection

- 狀態：已完成
- 實際修改或完成項目：只使用訓練集執行 Lasso L1 特徵選擇。將 `StandardScaler` 與 `Lasso` 放在 Pipeline，使用固定 `random_state=42` 的 5-fold `StratifiedGroupKFold`，確保標準化在各訓練 fold 內 fit，且相同完整列不跨 fold。搜尋 81 個 `alpha`（`1e-4` 至 `1`），以 one-standard-error 規則選擇在最小 CV RMSE 一個標準誤範圍內的最大 `alpha`。依非零係數選出子集後，只用該子集及完整訓練集重建普通線性回歸，並產生測試集預測；正式測試指標留待 Step 6。
- 測試指令或方法：完整重跑主程式與 `py_compile`；從新暫存目錄再跑一次。重新載入 Lasso selector，驗證其非零係數布林值與 feature_selection.csv 完全一致；重新載入特徵子集 OLS，驗證 317 筆預測逐筆一致（絕對容許 `1e-12`）；檢查預測皆為有限且不為常數；逐 bytes 比較兩次執行的五份表格；目視確認 Lasso 係數圖。
- 測試是否成功：成功；輸出 `step5_validation=PASS`、`selector_reload=PASS`、`selected_model_reload_predictions=PASS`、`reproducible_feature_selection=PASS`。
- 實際輸出結果：特徵由 11 個縮減為 4 個：`volatile acidity`、`total sulfur dioxide`、`sulphates`、`alcohol`。CV 最小 RMSE 為 0.650300；one-SE 上限為 0.663908；選定 `alpha=0.0630957`，其平均 CV RMSE 為 0.663722（標準差 0.032251）。子集 OLS 對 317 筆測試資料成功產生預測，範圍 4.674597–7.230680。這一步的前後比較為特徵數與交叉驗證選擇結果；基準／子集模型的同一測試集 MAE、RMSE、R² 比較於 Step 6 執行。
- 產生或修改檔案：`7115056106_hw2.py`、`outputs/tables/lasso_alpha_cv_results.csv`、`outputs/tables/feature_selection.csv`、`outputs/tables/feature_selection_summary.json`、`outputs/tables/selected_model_predictions.csv`、`outputs/tables/selected_model_coefficients.csv`、`outputs/models/lasso_feature_selector.joblib`、`outputs/models/selected_linear_regression.joblib`、`outputs/figures/lasso_feature_selection.png`、`TODO.md`、`PROJECT_LOG.md`。
- 尚未解決的問題或限制：one-SE 規則刻意用少量 CV RMSE 差異換取更精簡模型；是否改善未見資料的表現，必須由 Step 6 的固定測試集結果判定。Lasso 的非零係數代表在目前資料、網格及規則下入選，不等同因果關係。

## Step 6：Evaluation 與預測區間圖

- 狀態：已完成
- 實際修改或完成項目：在固定且未參與訓練／選模的 317 筆測試集計算基準 11 特徵 OLS 與精簡 4 特徵 OLS 的 MAE、RMSE、R²。以訓練集 fit statsmodels 精簡 OLS，對測試資料建立 95% 個別新觀測 prediction interval，另保留 mean response 的 95% confidence interval 數值以避免混淆。建立實際值／預測值比較圖、預測區間圖及殘差診斷圖；執行 Jarque–Bera、Breusch–Pagan、Durbin–Watson 與 Cook's distance 診斷。
- 測試指令或方法：完整執行及 `py_compile`；在新暫存目錄重跑。以 sklearn 獨立重算兩模型 MAE、RMSE、R²；驗證 statsmodels 預測平均與 sklearn 精簡模型逐筆一致、每筆預測平均位於其上下界之間、區間涵蓋率與 JSON 一致；逐 bytes 比較兩次執行的三份核心表格；以 Pillow 驗證三張 PNG 並目視檢查圖例、座標及內容。
- 測試是否成功：成功；輸出 `step6_validation=PASS`、`independent_metric_recalculation=PASS`、`prediction_interval_consistency=PASS`、`reproducible_evaluation_outputs=PASS`。
- 實際輸出結果：基準模型 MAE 0.503214、RMSE 0.657947、R² 0.341849；精簡模型 MAE 0.511868、RMSE 0.664149、R² 0.329384。精簡模型將特徵減少 63.64%，代價為 RMSE 增加 0.94%、MAE 增加 1.72%，因此基準模型的測試準確度略佳，不能宣稱選模提升表現。精簡模型 95% prediction interval 測試涵蓋率 0.946372，平均寬度 2.566784。Jarque–Bera p=`1.11e-08`，Breusch–Pagan LM p=`8.25e-06`，顯示殘差常態性與等變異假設均有違反；Cook's D 大於 `4/n` 者 78 筆，最大值 0.124842；Durbin–Watson 1.688651。
- 產生或修改檔案：`7115056106_hw2.py`、`outputs/tables/evaluation_metrics.csv`、`outputs/tables/selected_model_prediction_intervals.csv`、`outputs/tables/residual_diagnostics.json`、`outputs/figures/actual_vs_predicted.png`、`outputs/figures/selected_model_95_prediction_intervals.png`、`outputs/figures/selected_model_residual_diagnostics.png`、`TODO.md`、`PROJECT_LOG.md`。
- 尚未解決的問題或限制：`quality` 是 3–8 的離散順序評分，OLS 產生連續值且未限制範圍；殘差常態與等變異假設未通過，因此傳統 OLS 95% prediction interval 應視為基於模型假設的近似區間，不能解讀為精確保證。品質兩端樣本少且模型呈現向平均值收縮；Cook's distance 顯示部分觀測具影響力，但沒有資料依據時不任意刪除。Durbin–Watson 依賴資料列順序，本資料無明確時間順序，僅作描述、不過度解讀。

## Step 7：NotebookLM 研究與解法比較

- 狀態：已完成
- 實際修改或完成項目：保留使用者提供的 NotebookLM 原文與匯出 PDF 證據；逐一查核六筆來源的作者、年份、原始連結與可支持主張。由於黏連引用數字無法可靠還原，不猜測編號，而以六個具名直接連結重寫 391 字摘要。完成 OLS、Lasso 精簡 OLS、SVM、cumulative ordinal regression 與 modern ordinal classifier pooling 的比較，並區分來源直接證據、本作業實測結果及尚未實作的未來方法。
- 測試指令或方法：使用網路搜尋與原始資料庫／論文／期刊／作者課程頁查核；以 Python 讀取 Markdown，驗證修訂摘要至少 100 字、恰有六個不重複 HTTPS 來源連結、六筆來源名稱均存在、本作業兩個 RMSE 與 evaluation_metrics.csv 一致，且文件明確標示不可直接跨研究比較與未獲支持的 BIC 主張。
- 測試是否成功：成功；輸出 `step7_document_validation=PASS`、`summary_characters=391`、`unique_verified_source_links=6`、`project_metric_consistency=PASS`。
- 實際輸出結果：Cortez et al. (2009) 直接支持在其驗證與容忍度設定下 SVM 優於 multiple regression，並說明 MR 較容易解釋；UCI 支持 11 特徵、無缺失、有序且不平衡；Zhou et al. (2024) 支持 Lasso 較 stepwise 有更一致樣本外表現，以及較強收縮較精簡穩健，但其情境不是紅酒；Gambarota & Altoè (2024) 支持 ordinal cumulative model 明確處理有序反應；Lang 課程材料支持診斷影響點且不可無理由刪除；Rotenberg et al. (2026) 是 modern ordinal classifier pooling 預印本，未直接驗證本作業。原摘要的 BIC stepwise 極簡組合主張在六筆來源中缺乏直接證據，已移除。
- 產生或修改檔案：`materials/NOTEBOOKLM_RESEARCH.md`、`materials/NOTEBOOKLM_INPUT.md`、`TODO.md`、`PROJECT_LOG.md`。
- 尚未解決的問題或限制：NotebookLM 原始數字引用格式仍不可逆，但查核版已改用直接來源連結，不影響報告引用。跨研究的資料切分、調參與評估指標不同，不能用 Cortez 論文的 SVM 數字直接和本作業 RMSE 排名；ordinal regression 與 classifier pooling 未在本作業實作，只能列為有研究依據的替代方案。

## Step 8：完成 CRISP-DM 報告

- 狀態：已完成
- 實際修改或完成項目：以繁體中文完成 12 頁 CRISP-DM 報告，依序包含 Business Understanding、Data Understanding、Data Preparation、Modeling、Evaluation、Deployment；納入 Kaggle／UCI 來源、11 個特徵與目標、重複列群組切分、Lasso one-SE 特徵選擇、兩模型實測指標、95% 個別預測區間、殘差診斷、限制、六筆研究來源與解法比較。明確設置「GPT 輔助內容」及「NotebookLM 摘要」，並說明真實 GPT PDF 於 Step 9 作為附件納入。建立 ReportLab 產生器，使用系統 Arial Unicode 字型嵌入繁體中文與七張實際輸出圖。
- 測試指令或方法：`py_compile report/generate_report.py`；執行產生器；以 `file`、`shasum`、PDF header／EOF、Page object 及 Image XObject 檢查 PDF；用 Python 驗證六個 CRISP-DM 標題順序、GPT／NotebookLM 標示、NotebookLM 摘要至少 100 字、Kaggle URL、六項模型指標與 CSV 完全一致、四個入選特徵一致、區間涵蓋率一致、七張來源圖存在；以 `sips` 將首頁轉為 JPEG 並目視檢查中文字型與排版。
- 測試是否成功：成功；輸出 `step8_report_validation=PASS`、`crisp_dm_sections_in_order=PASS`、`report_metrics_match_outputs=PASS`、`pdf_structure=PASS`。
- 實際輸出結果：報告 PDF 1.4、12 頁、約 1.1 MB，嵌入七張來源圖；NotebookLM 摘要 391 字；SHA-256 為 `53aa398002cb672fa389d6bc1d897b1cac1154f6bf49065e84609a59a45fdacf`。首頁預覽顯示繁體中文、項目符號與摘要均可讀。
- 產生或修改檔案：`report/7115056106_hw2_report.md`、`report/generate_report.py`、`report/7115056106_hw2_report.pdf`、`TODO.md`、`PROJECT_LOG.md`。
- 尚未解決的問題或限制：GPT 對話 PDF 與 NotebookLM 匯出 PDF 仍位於使用者原始路徑，尚未複製、命名或與報告一起打包；此工作屬 Step 9。報告 PDF 是主報告，沒有宣稱已將附件內容合併成單一 PDF。

## Step 9：GPT 對話紀錄與檔案整理

- 狀態：已完成
- 實際修改或完成項目：建立 `submission/7115056106_hw2/`，整理主程式、主報告、原始及處理後資料、表格、模型、圖形、研究材料、管理紀錄、套件版本與執行說明。將使用者真實 GPT PDF 重新命名為 `7115056106_GPT_conversation.pdf`，NotebookLM 匯出重新命名為 `7115056106_NotebookLM_export.pdf`，均以二進位原樣複製。建立 `submission/7115056106_hw2.zip`。
- 測試指令或方法：用 Python 檢查八個必要檔案存在且非空、四個來源檔 SHA-256；以 `py_compile` 檢查 ZIP 內主程式及報告產生器語法；以 `file` 確認三份 PDF；以 `zip -r -X` 建檔並執行 `unzip -t` 完整 CRC 測試。
- 測試是否成功：成功；輸出 `submission_required_files=PASS`、`attachment_hashes=PASS`；`unzip -t` 對全部項目回報 `OK` 並顯示 `No errors detected in compressed data`。
- 實際輸出結果：繳交資料夾共 45 個檔案。GPT PDF 為 PDF 1.3、8 頁，SHA-256 `8e1b38cb3145646ca0d175e8fb79696c35b801d197aaff91be282b9db61d040e`；NotebookLM PDF 為 PDF 1.4、3 頁，SHA-256 `31aef74c2088a6929761793490d3654adba80b9ca90a36679a72eddf87624a35`；主報告 SHA-256 `53aa398002cb672fa389d6bc1d897b1cac1154f6bf49065e84609a59a45fdacf`；原始 CSV SHA-256 `d6a0d9bd24806944818795f22500c46cb6424cbff517aacda36595d3ed9b2daa`。
- 產生或修改檔案：`requirements.txt`、`SUBMISSION_README.md`、`submission/7115056106_hw2/` 內 45 個檔案、`submission/7115056106_hw2.zip`、`TODO.md`、`PROJECT_LOG.md`。
- 尚未解決的問題或限制：Step 10 尚須從獨立乾淨複本執行 ZIP 內主程式，比較重建輸出與報告數值，並再次驗證最終更新後的 ZIP。

## Step 10：最終驗收

- 狀態：已完成
- 實際修改或完成項目：將 Step 9 ZIP 解壓至獨立 `/private/tmp/aiot_hw2_final.aDoR1g`；把隨附 `outputs` 與 `data/processed` 移至備份名稱，從 ZIP 根目錄直接執行 `7115056106_hw2.py`，使程式在沒有既有輸出的狀態重建處理資料、模型、表格與圖片。比較重建結果、隨附成果及報告來源，最後同步已完成管理文件並重建 ZIP。
- 測試指令或方法：以獨立 Matplotlib 與 Python cache 路徑執行主程式；逐 bytes 比較重新產生與隨附的 16 份 tables 及 train/test CSV；用 Pillow 驗證七張重建 PNG；檢查報告來源包含重建的兩模型六項 MAE/RMSE/R² 與 prediction interval coverage；確認三份必要 PDF 存在且非空；重建最終 ZIP 後執行 CRC 測試及管理狀態檢查。
- 測試是否成功：成功；輸出 `step10_clean_extract_run=PASS`、`regenerated_tables_match=16`、`regenerated_splits_match=2`、`regenerated_figures_valid=7`、`report_metrics_consistency=PASS`、`required_pdfs_present=PASS`。首次工具呼叫在 Matplotlib 建立全新字型快取時超過 30 秒等待，但主程式隨後在同一獨立目錄正常完成，沒有模型或程式錯誤；驗證改以第二次唯讀檢查完成。
- 實際輸出結果：獨立重跑後的 16 份表格及兩份資料切分與 ZIP 隨附版本完全一致；七張圖皆可開啟；報告指標與重建結果一致；三份 PDF 均存在。全部 Step 0–10 均已完成。
- 產生或修改檔案：`TODO.md`、`PROJECT_LOG.md`，以及同步更新後的 `submission/7115056106_hw2/TODO.md`、`submission/7115056106_hw2/PROJECT_LOG.md`、`submission/7115056106_hw2.zip`。
- 尚未解決的問題或限制：無必要交付項目未完成。模型本身的統計限制（離散順序目標、殘差非常態、異質變異、品質兩端樣本少）已在報告揭露，不能因驗收成功而視為消失。
