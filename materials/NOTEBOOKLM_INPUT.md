# NotebookLM 研究材料（使用者提供）

- 提供日期：2026-10-08（Asia/Taipei）
- 狀態：已收到原文及 NotebookLM 匯出 PDF；Step 7 已完成來源與主張查核，修訂結果見 `materials/NOTEBOOKLM_RESEARCH.md`。
- 原則：以下內容照錄使用者提供文字，不宣稱由本程式或 AI agent 操作 NotebookLM 產生。

## 摘要原文

本研究探討運用多元線性回歸（MLR）預測葡萄牙 Vinho Verde 地區紅酒品質評分（共 1,599 筆樣本、11 個理化特徵）之適用性1。預測目標為多位專家盲測之 0–10 分中位數品質，資料分佈集中於中間等級25。在特徵選擇上，Lasso 回歸透過 L1 正則化懲罰與交叉驗證，較逐步回歸（Stepwise）具備更穩定的樣本外預測與選擇準確度，而搭配 BIC 的逐步回歸則能提供極簡變數組合6。模型效果由 MAE、RMSE 與 $R^2$ 等指標評估1112。然而，將線性回歸套用於離散順序資料存在理論限制，包含輸出連續小數、無評分邊界約束，以及評分等級非等距與殘差非常態等問題5。實證顯示，支持向量機（SVM）在容忍度評估下之預測準確率優於線性回歸，而順序回歸模型則更能契合離散等級之統計特性14。

## 使用者提供的實際引用來源名稱

1. *Modeling wine preferences by data mining from physicochemical properties - MIT CSAIL*
2. *Wine Quality - UCI Machine Learning Repository*
3. *Comparison of Lasso and Stepwise Regression in Psychological Data*
4. *Ordinal regression models made easy: A tutorial on parameter interpretation, data simulation and power analysis*
5. *Regression Assumptions & Diagnostics - Fundamental Techniques in Data Science with R - Kyle M. Lang*
6. *Classifier Pooling for Modern Ordinal Classification - arXiv*

## 待 Step 7 處理事項

- [x] 不猜測原文中的 `1`、`25`、`6`、`1112`、`5`、`14`，改以具名來源及直接連結取代。
- [x] 查核每筆來源的作者、年份與可存取連結。
- [x] 確認各研究主張的支持範圍，區分直接證據與本作業推論。
- [x] 移除六筆來源無法直接支持的 BIC stepwise 主張。

## NotebookLM 匯出 PDF

- 使用者提供日期：2026-10-08（Asia/Taipei）
- 原始路徑：`/Users/esleyw/Downloads/ACFrOgDRFA0k1B_EITfqUR8Nqvt4Mv_Xg8yrkFPlOpMVKbQuwverlGMwia58jnGsyjDDPgv8fospFU93JQvDQATqDPIwOgFpYeXpyfPA25BRtHk4RQ4JQm6V7UKypvZoctk1JxQM3banT2BtzJUM.pdf`
- 格式檢查：PDF 1.4，共 3 頁，約 129 KB。
- SHA-256：`31aef74c2088a6929761793490d3654adba80b9ca90a36679a72eddf87624a35`
- 目前環境沒有 `pypdf`、`PyPDF2`、`pdfplumber` 或 `fitz`，因此本次只完成檔案完整性與格式檢查，尚未宣稱已擷取或核對 PDF 內文。
