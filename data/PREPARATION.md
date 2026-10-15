# Step 3：Data Preparation 資料準備決策

## 1. 資料集規格與品質處理

- **資料集來源**：Kaggle Playground Series Season 4 Episode 5 (Regression with a Flood Prediction Dataset)。
- **資料規模**：原始下載之競賽訓練集為 1,117,957 筆。為兼顧執行效能、重複驗證速度與 GitHub 檔案傳輸限制（< 25MB），使用固定亂數種子（`random_state=42`）抽取 50,000 筆具統計代表性之樣本儲存於 `data/raw/train.csv`（2.5 MB）。
- **欄位結構**：
  - `id`：觀測識別碼，僅作索引追蹤，於前處理與模型特徵矩陣中嚴格剔除。
  - **20 個原始輸入特徵**：`MonsoonIntensity`、`TopographyDrainage`、`RiverManagement`、`Deforestation`、`Urbanization`、`ClimateChange`、`DamsQuality`、`Siltation`、`AgriculturalPractices`、`Encroachments`、`IneffectiveDisasterPreparedness`、`DrainageSystems`、`CoastalVulnerability`、`Landslides`、`Watersheds`、`DeterioratingInfrastructure`、`PopulationScore`、`WetlandLoss`、`InadequatePlanning`、`PoliticalFactors`。
  - **目標變數**：`FloodProbability`（連續型浮點數，機率值區間 [0.285, 0.725]）。
- **特徵數量查核**：原始輸入特徵共 20 個，精確滿足作業規範「10–20 個原始特徵」及追加規格「13 < features < 40」。
- **缺失值檢驗**：50,000 筆樣本中，所有 22 欄之缺失值總數為 0，因此不執行缺失值插補。
- **重複值檢驗**：在排除 `id` 後檢驗 20 個特徵及目標值之組合，重複列為 0 筆。
- **類別編碼**：20 個特徵均為離散數值評分（整數），目標為連續機率數值，無需進行類別編碼（One-Hot / Ordinal Encoding）。

## 2. 切分策略（Data Splitting Strategy）

- **訓練／測試切分**：
  - 本資料集目標為連續數值（非分類類別標籤），且觀測值彼此獨立，無群組或時間序列相依性。
  - 採用標準 80/20 切分（`train_test_split`，固定 `random_state=42`，`shuffle=True`）。
  - 切分結果：訓練集 40,000 筆（80.0%），獨立測試集 10,000 筆（20.0%）。
  - 分別儲存於 `data/processed/train.csv` 與 `data/processed/test.csv`。

## 3. 防範資料洩漏（Leakage Prevention）

- **特徵標準化機制**：
  - 基準多元線性回歸（Baseline OLS）直接使用未縮放原始特徵，係數具備直觀之物理單位意義（每增加 1 分之洪水機率增量）。
  - Lasso 特徵選擇需進行標準化（Standardization, Z-score）。為防止測試資訊外洩，標準化嚴格封裝於 `sklearn.pipeline.Pipeline([('scaler', StandardScaler()), ('lasso', Lasso())])` 中。
  - 5-fold 交叉驗證中，`StandardScaler` 僅在各 fold 之訓練子集（train-fold）fit，隨後 transform 至驗證子集（val-fold）。
  - 最終選定特徵後之回歸模型，僅在 40,000 筆訓練集上擬合，並在從未參與特徵選擇或模型訓練的 10,000 筆獨立測試集上進行泛化評估與 95% 預測區間檢定。

## 4. 歷史紅酒資料集替換說明

原作業採用之 UCI Red Wine Quality 資料集僅包含 11 個原始特徵（不符 14–20 特徵新規）。舊版切分採用之 `StratifiedGroupKFold` 係因應紅酒 240 筆重複列之過渡解法。本次 S4E5 資料集特徵數達標（20 個），無重複列與洩漏風險，全面改採標準連續回歸切分架構。
