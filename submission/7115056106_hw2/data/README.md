# 資料來源與重現資訊

## Red Wine Quality

- Kaggle 資料集名稱：Red Wine Quality
- Kaggle 頁面：https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009
- 下載 API：https://www.kaggle.com/api/v1/datasets/download/uciml/red-wine-quality-cortez-et-al-2009
- 下載日期：2026-10-08（Asia/Taipei）
- 原始檔案：`raw/winequality-red.csv`
- CSV SHA-256：`d6a0d9bd24806944818795f22500c46cb6424cbff517aacda36595d3ed9b2daa`
- 實際資料列數：1,599（不含標題列）
- 實際欄位數：12（11 個輸入特徵及 1 個目標）
- 預測目標：`quality`

### 輸入特徵（11 個）

1. `fixed acidity`
2. `volatile acidity`
3. `citric acid`
4. `residual sugar`
5. `chlorides`
6. `free sulfur dioxide`
7. `total sulfur dioxide`
8. `density`
9. `pH`
10. `sulphates`
11. `alcohol`

## 研究問題

使用紅酒的 11 個理化測量特徵建立多元線性回歸模型，預測感官品質分數 `quality`，並比較特徵選擇前後的測試集表現及預測區間。

`quality` 是有序、離散的評分；本作業依指定方法將它作為數值型回歸目標，但後續評估必須討論線性模型可能產生小數預測、線性假設未必成立等限制。
