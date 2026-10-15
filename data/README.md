# 資料來源與重現資訊

## 1. 現行資料集：Kaggle Playground Series S4E5（洪水機率預測，Flood Prediction）

- **Kaggle 競賽名稱**：Playground Series Season 4, Episode 5 - Regression with a Flood Prediction Dataset
- **Kaggle 頁面**：https://www.kaggle.com/competitions/playground-series-s4e5
- **取得方式**：透過 Kaggle 官方 API 與使用者授權 Token 取得完整競賽壓縮包 `playground-series-s4e5.zip`（總筆數 1,117,957 筆）。
- **取樣與重現規格**：為符合 GitHub 單檔儲存上限（避免超過 50MB 警示）並兼顧分析效能與重現性，以固定隨機亂數種子（`random_state=42`）抽取具高度統計代表性之 **50,000 筆**樣本保存於 `data/raw/train.csv`。經實測母體與樣本的平均值、標準差與相關矩陣完全一致。
- **原始檔案**：`data/raw/train.csv`
- **CSV SHA-256**：`d61303b070d08ab32df43978c450e6d399e2f5d83d0db8c0d26e478ddbed811f`
- **實際資料列數**：50,000（不含標題列）
- **總欄位數**：22（1 個 ID、20 個輸入特徵、1 個目標變數）
- **排除欄位**：`id`（樣本識別序號，嚴格排除於模型輸入特徵外）
- **預測目標 (Target)**：`FloodProbability`（連續型數值變數，範圍約在 0.285 至 0.725 之間，代表區域發生洪水之機率）

### 原始輸入特徵（恰好 20 個，符合 14–20 個特徵規格）

1. `MonsoonIntensity`：季風降雨強度
2. `TopographyDrainage`：地形與天然排水能力
3. `RiverManagement`：河流疏濬與防洪管理水平
4. `Deforestation`：森林砍伐程度
5. `Urbanization`：都市化與地表不透水比例
6. `ClimateChange`：氣候變遷衝擊指數
7. `DamsQuality`：水壩與蓄水設施工程品質
8. `Siltation`：河道淤積程度
9. `AgriculturalPractices`：農業水土保持實務指數
10. `Encroachments`：河川地侵占與違章建築程度
11. `IneffectiveDisasterPreparedness`：防災整備不足程度
12. `DrainageSystems`：人工排水系統容量與效能
13. `CoastalVulnerability`：海岸暴潮易受衝擊程度
14. `Landslides`：土石流與山崩易發程度
15. `Watersheds`：集水區流域健康指標
16. `DeterioratingInfrastructure`：水利基礎設施老化惡化程度
17. `PopulationScore`：受災風險區域人口密度分數
18. `WetlandLoss`：天然濕地滯洪面積縮減率
19. `InadequatePlanning`：土地利用規劃不足程度
20. `PoliticalFactors`：治水政策與治理因素評分

### 研究問題

使用 20 個客觀環境、基礎建設與社會治理特徵建立多元線性回歸（Multiple Linear Regression）模型，預測連續型洪水發生機率 `FloodProbability`：
1. 20 個環境與治理特徵能否建立高可解釋性且精準的線性基準預測模型？
2. 透過 Lasso（L1 Penalty）特徵選擇與交叉驗證 1-SE 規則，能否識別出對洪水機率最關鍵的風險因子子集？
3. 在此連續型回歸問題中，殘差假設（常態性、等變異性與自相關性）的檢定結果為何？95% 預測區間的覆蓋率與精確度表現如何？

---

## 2. 舊版資料集紀錄（歷史保留存檔）：Red Wine Quality

- **Kaggle 頁面**：https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009
- **檔案**：`data/raw/winequality-red.csv`
- **特徵數**：11 個理化特徵（因未達 14–20 個特徵標準，本專案已正式升級為 S4E5 洪水資料集，舊檔與歷史記錄保留以供查核）。
