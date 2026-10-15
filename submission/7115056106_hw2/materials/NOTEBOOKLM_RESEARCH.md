# NotebookLM 研究摘要與解法比較

## 材料來源與處理方式

本節依使用者實際提供的 NotebookLM 摘要、六筆來源名稱及三頁匯出 PDF 整理。原始摘要的 `1`、`25`、`6`、`1112`、`5`、`14` 在純文字貼上後失去引用分隔，無法可靠還原成原始編號，因此不猜測數字對應，而將可查證的主張改成具名超連結。查核日期為 2026-10-08（Asia/Taipei）。

## NotebookLM 摘要（查核修訂版，超過 100 字）

本研究探討以多元線性回歸預測葡萄牙 Vinho Verde 紅酒品質的適用性。UCI 資料說明指出此資料包含 11 個理化輸入，品質為 0–10 分的感官評分；類別具有順序且分布不平衡，因此可視為回歸或分類問題，也適合研究特徵選擇。原始研究以多元回歸、神經網路及支持向量機比較，結果顯示在其驗證設計與容忍度指標下，SVM 優於多元回歸，但需要較高計算成本。Lasso 與逐步回歸的模擬研究則顯示，Lasso 的樣本外預測較一致，而較強的收縮可提高精簡度與穩定性；該研究來自心理資料情境，不能直接當成紅酒資料的實證結論。品質分數是有序類別，ordinal cumulative model 會直接建模各等級的累積機率與門檻，因此在統計形式上比把分數當等距連續值更貼近資料性質。本作業仍依題目使用 OLS，並以 MAE、RMSE、R²、殘差診斷及 95% 個別預測區間呈現其效果與限制。

## 六筆來源查核

1. **Cortez, Cerdeira, Almeida, Matos, and Reis (2009), “Modeling wine preferences by data mining from physicochemical properties.”**  
   [MIT CSAIL 保存的論文全文](https://projects.csail.mit.edu/wiki/pub/Evodesign/SensoryEvaluationsDatabase/winequality09.pdf)，DOI：`10.1016/j.dss.2009.05.016`。直接支持資料包含 1,599 筆紅酒、以回歸保留品質順序、以誤差容忍度評估，以及在該研究設定下 SVM 優於多元回歸與神經網路。論文亦指出多元回歸較容易解釋，而 SVM 計算成本較高。

2. **Cortez et al. (2009), Wine Quality, UCI Machine Learning Repository.**  
   [UCI Wine Quality 資料頁](https://archive.ics.uci.edu/ml/datasets/wine%20quality)，DOI：`10.24432/C56S3T`。直接支持 11 個實數型理化特徵、感官品質目標、無缺失值，以及品質類別有順序且不平衡；UCI 明確指出可作為 classification 或 regression，並建議研究 feature selection。

3. **Zhou, Chahal, Gotlib, and Liu (2024), “Comparison of Lasso and Stepwise Regression in Psychological Data.”**  
   [Methodology 原始期刊頁面](https://meth.psychopen.eu/index.php/meth/article/view/11523)，DOI：`10.5964/meth.11523`。其 Monte Carlo 模擬與實證示例顯示 Lasso 的樣本內選擇較準確、樣本外預測一致性優於 stepwise；較強收縮的 Lasso 較精簡且對抽樣變異更穩健。此來源不是紅酒研究，僅能作為本作業採 Lasso 與 one-standard-error 類型精簡原則的方法依據。

4. **Gambarota and Altoè (2024), “Ordinal regression models made easy: A tutorial on parameter interpretation, data simulation and power analysis.”**  
   [International Journal of Psychology 原始期刊頁面](https://onlinelibrary.wiley.com/doi/10.1002/ijop.13243)，DOI：`10.1002/ijop.13243`。文章將 ordinal regression 定義為明確考慮反應變數順序、而非把它視為等距數值的模型，並說明 cumulative model 以潛在變數及門檻表示有序結果。此來源支持將 ordinal regression 列為後續方法，而不表示它已在本作業資料上獲得較佳測試成績。

5. **Kyle M. Lang, “Regression Assumptions & Diagnostics,” Fundamental Techniques in Data Science with R.**  
   [原始課程投影片](https://www.kylemlang.com/fundamentals/wk5/lecture/assumptions.pdf)。內容支持檢查線性模型假設、離群值、高槓桿及影響觀測，也提醒即使觀測具有影響力，若無合理依據仍不能任意刪除；可考慮 robust regression。這與本作業保留極端觀測並報告 Cook's distance 的處理一致。

6. **Rotenberg, Faria, and Caffo (2026), “Classifier Pooling for Modern Ordinal Classification.”**  
   [arXiv 原始預印本](https://arxiv.org/abs/2603.17278)，arXiv：`2603.17278`。文章提出可將一般分類器包裝成 ordinal classification 的方法，並在多個真實資料集上呈現其優勢，特別是樣本較少或類別較多的情境。這是一篇 2026 年預印本，並未直接驗證本作業的紅酒切分，因此只列為新式替代方案。

## 本作業與其他解法比較

| 方法 | 來源或本作業證據 | 優點 | 限制／本作業定位 |
|---|---|---|---|
| 11 特徵 OLS | 本作業固定測試集：MAE 0.503214、RMSE 0.657947、R² 0.341849 | 最佳測試指標、容易解釋、符合指定方法 | 連續且無界輸出不完全符合有序評分；常態與等變異假設未通過 |
| Lasso 選擇後 4 特徵 OLS | 本作業固定測試集：MAE 0.511868、RMSE 0.664149、R² 0.329384 | 特徵減少 63.64%，準確度只小幅下降；較易部署與解釋 | 沒有改善測試準確度；選中特徵不代表因果 |
| SVM regression | Cortez et al. (2009) 在其交叉驗證及容忍度設定下優於 multiple regression | 可表示非線性關係，原始紅酒研究結果較佳 | 較耗計算且較難解釋；因切分及指標不同，不能把原論文數字與本作業 RMSE 直接比較 |
| Cumulative ordinal regression | Gambarota & Altoè (2024) 的方法論 | 直接尊重品質等級順序與門檻，輸出各等級機率 | 需檢查 proportional-odds 等假設；本作業未實際 fit，不能聲稱表現更好 |
| Modern ordinal classifier pooling | Rotenberg et al. (2026) 預印本 | 可結合現代分類器並利用類別順序 | 較新、可解釋性及實作複雜度較高；未在本作業資料上驗證 |

## 綜合結論

本作業應把 11 特徵 OLS 視為測試預測表現較佳的指定基準，把 4 特徵 OLS 視為準確度略降但更精簡的替代方案。SVM 是原始酒品質研究中較強的非線性解法，而 cumulative ordinal regression 在資料型態上更自然；兩者可作為未來比較模型，不能在未用相同資料切分與指標實測前宣稱優於本作業模型。原 NotebookLM 摘要中的 BIC stepwise 極簡組合主張未在上述六筆來源中找到足夠直接證據，因此不納入查核修訂版。
