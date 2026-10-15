# Kaggle Playground S4E5 洪水預測（Flood Prediction）NotebookLM 研究指引

> **狀態**：待使用者提供真實 NotebookLM 匯出檔案（Pending User Input）  
> **規範聲明**：本專案嚴格遵守誠信與真實性原則，**嚴禁以 GPT 偽造 NotebookLM 產出內容**。本文件提供建議之研究文獻來源、提問方向與匯出步驟，供使用者於 NotebookLM 操作並匯出真實 PDF。

---

## 1. 建議匯入 NotebookLM 之研究來源 (Candidate Sources)

建議在 [Google NotebookLM](https://notebooklm.google.com/) 建立名為「Flood Prediction MLR & Feature Selection」之筆記本，並加入以下 4–6 篇公開學術文獻或技術文檔網址／PDF：

1. **Kaggle 官方競賽頁面與資料說明**
   - 來源：[Kaggle Playground Series s4e5: Regression with a Flood Prediction Dataset](https://www.kaggle.com/competitions/playground-series-s4e5)
   - 說明：涵蓋 20 項理化/環境指標與連續型洪水發生機率目標。
2. **洪水易感性評估與多元線性回歸比較**
   - 論文例：*Application of Multiple Linear Regression and Machine Learning Models for Regional Flood Risk Assessment* (例如 Hydrological Sciences Journal 或 Water Resources Management 相關論文)。
   - 說明：探討地形、降雨強度（MonsoonIntensity）與排水系統（DrainageSystems）對洪水預測之線性與非線性關聯。
3. **高維特徵選擇與收縮估計（Lasso vs OLS）**
   - 論文例：*Tibshirani, R. (1996). Regression shrinkage and selection via the lasso. Journal of the Royal Statistical Society: Series B.*
   - 說明：說明 L1 正則化在多特徵環境下篩選關鍵致災因子的統計性質與稀疏解優勢。
4. **模型評估與預測區間（Prediction Intervals in Environmental Modeling）**
   - 文獻例：環境統計學中針對未來觀測建立 95% 個別預測區間之常態性與等變異性假設檢定。

---

## 2. 建議向 NotebookLM 提問之問題 (Prompt Questions)

可向 NotebookLM 提出以下核心問題：
1. 「在區域洪水風險或機率預測中，多元線性回歸（MLR）相較於樹模型（如 LightGBM、XGBoost）的主要優缺點為何？在可解釋性與計算複雜度上有何價值？」
2. 「面對 20 個環境與基礎設施致災特徵時，Lasso 正則化（L1 Penalty）如何協助辨識最重要的少數關鍵特徵？其係數收縮對多重共線性的處理效果如何？」
3. 「在環境回歸模型中，殘差診斷（如 Durbin-Watson、Breusch-Pagan 與 Jarque-Bera）對於詮釋 95% 預測區間可靠性有何重要性？若未通過假設該如何解讀？」

---

## 3. 匯出與繳交準備 (Export Instructions)

完成對話與筆記彙整後：
1. 從 NotebookLM 介面將對話與筆記匯出為 PDF 檔案。
2. 將匯出的 PDF 重新命名為 `7115056106_NotebookLM_export.pdf`。
3. 提供至少 100 字經來源查核之摘要，記錄於專案中。
4. 本專案將自動整合並執行 SHA-256 完整性校驗。
