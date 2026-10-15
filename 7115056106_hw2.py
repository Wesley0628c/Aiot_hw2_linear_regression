"""7115056106 HW2：Kaggle Playground S4E5 洪水預測（Flood Prediction）多元線性回歸分析。

分析流程：CRISP-DM
- Step 2 Data Understanding
- Step 3 Data Preparation
- Step 4 基準線性回歸模型（20 特徵）
- Step 5 Lasso 特徵選擇與重構模型
- Step 6 模型評估與 95% 預測區間
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from joblib import dump
from sklearn.linear_model import Lasso, LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson, jarque_bera

ID_COLUMN = "id"
TARGET = "FloodProbability"
FEATURE_COLUMNS = [
    "MonsoonIntensity",
    "TopographyDrainage",
    "RiverManagement",
    "Deforestation",
    "Urbanization",
    "ClimateChange",
    "DamsQuality",
    "Siltation",
    "AgriculturalPractices",
    "Encroachments",
    "IneffectiveDisasterPreparedness",
    "DrainageSystems",
    "CoastalVulnerability",
    "Landslides",
    "Watersheds",
    "DeterioratingInfrastructure",
    "PopulationScore",
    "WetlandLoss",
    "InadequatePlanning",
    "PoliticalFactors",
]
EXPECTED_COLUMNS = [ID_COLUMN] + FEATURE_COLUMNS + [TARGET]


def load_data(data_path: Path) -> pd.DataFrame:
    """讀取原始資料並驗證本作業預期的資料結構。"""
    data = pd.read_csv(data_path)
    if data.columns.tolist() != EXPECTED_COLUMNS:
        raise ValueError(f"欄位與預期不符：{data.columns.tolist()}")
    if data.empty:
        raise ValueError("資料集不得為空。")
    return data


def save_data_understanding(data: pd.DataFrame, output_dir: Path) -> None:
    """輸出描述統計、品質分布、缺失值摘要與探索性圖表。"""
    tables_dir = output_dir / "tables"
    figures_dir = output_dir / "figures"
    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    features = [column for column in FEATURE_COLUMNS]
    summary = {
        "row_count": int(len(data)),
        "column_count": int(data.shape[1]),
        "feature_count": int(len(features)),
        "id_column": ID_COLUMN,
        "target": TARGET,
        "column_names": data.columns.tolist(),
        "dtypes": {column: str(dtype) for column, dtype in data.dtypes.items()},
        "missing_value_count": int(data.isna().sum().sum()),
        "duplicate_row_count": int(data.duplicated(subset=features + [TARGET]).sum()),
        "target_min": float(data[TARGET].min()),
        "target_max": float(data[TARGET].max()),
        "target_mean": float(data[TARGET].mean()),
        "target_median": float(data[TARGET].median()),
        "target_std": float(data[TARGET].std()),
    }
    (tables_dir / "data_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    desc = data[features + [TARGET]].describe().T
    desc["skewness"] = data[features + [TARGET]].skew()
    desc.to_csv(tables_dir / "descriptive_statistics.csv")

    quality_summary = pd.DataFrame(
        {
            "column": data.columns,
            "dtype": [str(dtype) for dtype in data.dtypes],
            "missing_count": data.isna().sum().values,
            "missing_pct": (data.isna().mean() * 100).round(4).values,
            "unique_values": [data[col].nunique() for col in data.columns],
        }
    )
    quality_summary.to_csv(tables_dir / "column_quality_summary.csv", index=False)

    # 目標分布表格（分位數與統計分布）
    percentiles = np.linspace(0.05, 0.95, 19)
    target_dist_table = pd.DataFrame(
        {
            "percentile": [f"{p*100:.0f}%" for p in percentiles],
            "value": [float(data[TARGET].quantile(p)) for p in percentiles],
        }
    )
    target_dist_table.to_csv(tables_dir / "target_distribution.csv", index=False)

    # 1. 目標分布直方圖與 KDE
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(data[TARGET], kde=True, color="#0A9396", bins=30, ax=ax)
    ax.axvline(data[TARGET].mean(), color="#9B2226", linestyle="--", linewidth=1.5, label=f"Mean: {data[TARGET].mean():.4f}")
    ax.axvline(data[TARGET].median(), color="#EE9B00", linestyle=":", linewidth=1.5, label=f"Median: {data[TARGET].median():.4f}")
    ax.set(title=f"Distribution of Target Variable: {TARGET}", xlabel=TARGET, ylabel="Count")
    ax.legend()
    fig.tight_layout()
    fig.savefig(figures_dir / "target_distribution.png", dpi=160)
    plt.close(fig)

    # 2. 相關係數熱力圖 (20 特徵 + 目標)
    fig, ax = plt.subplots(figsize=(14, 12))
    corr = data[features + [TARGET]].corr()
    sns.heatmap(corr, cmap="vlag", center=0, annot=False, fmt=".2f", cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title(f"Correlation Heatmap ({len(features)} Features and {TARGET})", fontsize=14, pad=12)
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.yticks(fontsize=9)
    fig.tight_layout()
    fig.savefig(figures_dir / "correlation_heatmap.png", dpi=160)
    plt.close(fig)

    # 3. 20 個特徵直方圖分布
    fig, axes = plt.subplots(4, 5, figsize=(18, 14))
    axes = axes.flatten()
    for i, feature in enumerate(features):
        ax = axes[i]
        sns.histplot(data[feature], bins=15, color="#0A9396", ax=ax, discrete=True)
        ax.set_title(feature, fontsize=10)
        ax.set_xlabel("")
        ax.set_ylabel("Count", fontsize=8)
        ax.tick_params(labelsize=8)
    fig.suptitle("Histograms of 20 Physiochemical and Environmental Features", fontsize=15, y=0.995)
    fig.tight_layout()
    fig.savefig(figures_dir / "feature_distributions.png", dpi=160)
    plt.close(fig)

    print(json.dumps(summary, ensure_ascii=False, indent=2))


def prepare_data(data: pd.DataFrame, processed_dir: Path, output_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """執行訓練集與測試集切分（80/20，固定 random_state=42）。"""
    tables_dir = output_dir / "tables"
    processed_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)

    # 連續目標採用隨機切分，固定 random_state=42，測試集比例為 20%
    train_data, test_data = train_test_split(
        data, test_size=0.2, random_state=42, shuffle=True
    )
    train_data = train_data.sort_values(ID_COLUMN).reset_index(drop=True)
    test_data = test_data.sort_values(ID_COLUMN).reset_index(drop=True)

    features = FEATURE_COLUMNS
    train_data.to_csv(processed_dir / "train.csv", index=False)
    test_data.to_csv(processed_dir / "test.csv", index=False)

    split_summary = {
        "strategy": "train_test_split (80% train, 20% test)",
        "random_state": 42,
        "original_rows": int(len(data)),
        "train_rows": int(len(train_data)),
        "test_rows": int(len(test_data)),
        "test_fraction": float(len(test_data) / len(data)),
        "missing_values_train": int(train_data.isna().sum().sum()),
        "missing_values_test": int(test_data.isna().sum().sum()),
        "train_target_mean": float(train_data[TARGET].mean()),
        "train_target_std": float(train_data[TARGET].std()),
        "test_target_mean": float(test_data[TARGET].mean()),
        "test_target_std": float(test_data[TARGET].std()),
    }
    (tables_dir / "split_summary.json").write_text(
        json.dumps(split_summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(json.dumps({"data_preparation": split_summary}, ensure_ascii=False, indent=2))
    return train_data, test_data


def train_baseline_model(
    train_data: pd.DataFrame, test_data: pd.DataFrame, output_dir: Path
) -> None:
    """使用全部 20 個特徵訓練普通最小平方法（OLS）基準模型。"""
    tables_dir = output_dir / "tables"
    models_dir = output_dir / "models"
    tables_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)

    features = FEATURE_COLUMNS
    x_train = train_data[features]
    y_train = train_data[TARGET]
    x_test = test_data[features]

    baseline_model = LinearRegression(fit_intercept=True)
    baseline_model.fit(x_train, y_train)

    predictions = baseline_model.predict(x_test)
    prediction_df = pd.DataFrame(
        {
            ID_COLUMN: test_data[ID_COLUMN],
            f"actual_{TARGET}": test_data[TARGET],
            f"predicted_{TARGET}": predictions,
            "residual": test_data[TARGET] - predictions,
        }
    )
    prediction_df.to_csv(tables_dir / "baseline_predictions.csv", index=False)

    coefficients_table = pd.DataFrame(
        {
            "feature": features,
            "coefficient": baseline_model.coef_,
        }
    )
    coefficients_table.to_csv(tables_dir / "baseline_coefficients.csv", index=False)

    baseline_summary = {
        "model": "sklearn.linear_model.LinearRegression",
        "fit_intercept": True,
        "features": features,
        "feature_count": len(features),
        "train_rows": int(len(train_data)),
        "test_rows": int(len(test_data)),
        "intercept": float(baseline_model.intercept_),
        "prediction_count": int(len(predictions)),
        "prediction_min": float(predictions.min()),
        "prediction_max": float(predictions.max()),
        "prediction_mean": float(predictions.mean()),
    }
    (tables_dir / "baseline_model_summary.json").write_text(
        json.dumps(baseline_summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    dump(baseline_model, models_dir / "baseline_linear_regression.joblib")

    print(json.dumps({"baseline_model": baseline_summary}, ensure_ascii=False, indent=2))


def select_features_and_refit(
    train_data: pd.DataFrame, test_data: pd.DataFrame, output_dir: Path
) -> None:
    """在訓練集內以 Pipeline 執行標準化與 Lasso 特徵篩選，並以入選特徵重構 OLS。"""
    tables_dir = output_dir / "tables"
    models_dir = output_dir / "models"
    figures_dir = output_dir / "figures"
    tables_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    features = FEATURE_COLUMNS
    x_train = train_data[features]
    y_train = train_data[TARGET]
    x_test = test_data[features]

    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    alpha_candidates = np.logspace(-5, -2, 50)
    cv_records = []

    for alpha in alpha_candidates:
        fold_rmses = []
        for train_idx, val_idx in kf.split(x_train):
            pipeline = Pipeline(
                [
                    ("scaler", StandardScaler()),
                    ("lasso", Lasso(alpha=alpha, random_state=42, max_iter=5000)),
                ]
            )
            pipeline.fit(x_train.iloc[train_idx], y_train.iloc[train_idx])
            val_preds = pipeline.predict(x_train.iloc[val_idx])
            fold_rmses.append(np.sqrt(mean_squared_error(y_train.iloc[val_idx], val_preds)))

        cv_records.append(
            {
                "alpha": float(alpha),
                "cv_rmse_mean": float(np.mean(fold_rmses)),
                "cv_rmse_std": float(np.std(fold_rmses, ddof=1)),
                "cv_rmse_se": float(np.std(fold_rmses, ddof=1) / np.sqrt(len(fold_rmses))),
            }
        )

    cv_results_df = pd.DataFrame(cv_records)
    cv_results_df.to_csv(tables_dir / "lasso_alpha_cv_results.csv", index=False)

    min_row = cv_results_df.loc[cv_results_df["cv_rmse_mean"].idxmin()]
    one_se_threshold = min_row["cv_rmse_mean"] + min_row["cv_rmse_se"]
    eligible = cv_results_df[cv_results_df["cv_rmse_mean"] <= one_se_threshold]
    selected_alpha = float(eligible["alpha"].max())

    selector_pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("lasso", Lasso(alpha=selected_alpha, random_state=42, max_iter=5000)),
        ]
    )
    selector_pipeline.fit(x_train, y_train)
    standardized_coefficients = selector_pipeline.named_steps["lasso"].coef_

    # 若係數絕對值大於 1e-4 則入選
    selected_features = [
        feature
        for feature, coef in zip(features, standardized_coefficients)
        if abs(coef) > 1e-4
    ]

    # 若極端情況下全部被篩除，則回退至最小 RMSE 的 alpha
    if not selected_features:
        selected_alpha = float(min_row["alpha"])
        selector_pipeline = Pipeline(
            [
                ("scaler", StandardScaler()),
                ("lasso", Lasso(alpha=selected_alpha, random_state=42, max_iter=5000)),
            ]
        )
        selector_pipeline.fit(x_train, y_train)
        standardized_coefficients = selector_pipeline.named_steps["lasso"].coef_
        selected_features = [
            feature
            for feature, coef in zip(features, standardized_coefficients)
            if abs(coef) > 1e-4
        ]

    # 以入選特徵在完整訓練集重構普通最小平方法模型
    selected_model = LinearRegression(fit_intercept=True)
    selected_model.fit(train_data[selected_features], y_train)
    selected_predictions = selected_model.predict(test_data[selected_features])

    prediction_df = pd.DataFrame(
        {
            ID_COLUMN: test_data[ID_COLUMN],
            f"actual_{TARGET}": test_data[TARGET],
            f"predicted_{TARGET}": selected_predictions,
            "residual": test_data[TARGET] - selected_predictions,
        }
    )
    prediction_df.to_csv(tables_dir / "selected_model_predictions.csv", index=False)

    selection_table = pd.DataFrame(
        {
            "feature": features,
            "standardized_lasso_coefficient": standardized_coefficients,
            "selected": [feature in selected_features for feature in features],
        }
    )
    selection_table.to_csv(tables_dir / "feature_selection.csv", index=False)

    refit_coefficients = pd.DataFrame(
        {"feature": selected_features, "coefficient": selected_model.coef_}
    )
    refit_coefficients.to_csv(tables_dir / "selected_model_coefficients.csv", index=False)

    selection_summary = {
        "method": "StandardScaler + Lasso with 5-fold CV",
        "selection_rule": "largest alpha within one standard error of minimum CV RMSE",
        "random_state": 42,
        "alpha_candidates": len(alpha_candidates),
        "minimum_cv_rmse": float(min_row["cv_rmse_mean"]),
        "one_se_threshold": float(one_se_threshold),
        "selected_alpha": selected_alpha,
        "features_before": features,
        "feature_count_before": len(features),
        "features_after": selected_features,
        "feature_count_after": len(selected_features),
        "refit_model": "sklearn.linear_model.LinearRegression",
        "train_rows": int(len(train_data)),
        "test_prediction_count": int(len(selected_predictions)),
        "test_prediction_min": float(selected_predictions.min()),
        "test_prediction_max": float(selected_predictions.max()),
    }
    (tables_dir / "feature_selection_summary.json").write_text(
        json.dumps(selection_summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    dump(selector_pipeline, models_dir / "lasso_feature_selector.joblib")
    dump(selected_model, models_dir / "selected_linear_regression.joblib")

    # Lasso 標準化係數長條圖
    fig, ax = plt.subplots(figsize=(10, 7))
    plot_data = selection_table.sort_values("standardized_lasso_coefficient")
    bar_colors = ["#0A9396" if s else "#B7B7B7" for s in plot_data["selected"]]
    ax.barh(plot_data["feature"], plot_data["standardized_lasso_coefficient"], color=bar_colors)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_title(f"Lasso Feature Selection Standardized Coefficients (alpha={selected_alpha:.5g})", fontsize=12)
    ax.set_xlabel("Standardized Coefficient", fontsize=10)
    ax.set_ylabel("Feature", fontsize=10)
    fig.tight_layout()
    fig.savefig(figures_dir / "lasso_feature_selection.png", dpi=160)
    plt.close(fig)

    print(json.dumps({"feature_selection": selection_summary}, ensure_ascii=False, indent=2))


def evaluate_models(
    train_data: pd.DataFrame, test_data: pd.DataFrame, output_dir: Path
) -> None:
    """使用獨立測試集評估模型指標，計算 95% 預測區間與殘差統計診斷。"""
    tables_dir = output_dir / "tables"
    figures_dir = output_dir / "figures"
    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    baseline_predictions = pd.read_csv(tables_dir / "baseline_predictions.csv")
    selected_predictions = pd.read_csv(tables_dir / "selected_model_predictions.csv")
    selection_summary = json.loads(
        (tables_dir / "feature_selection_summary.json").read_text(encoding="utf-8")
    )
    baseline_summary = json.loads(
        (tables_dir / "baseline_model_summary.json").read_text(encoding="utf-8")
    )

    selected_features = selection_summary["features_after"]
    actual = test_data[TARGET].to_numpy()

    baseline_feature_count = int(baseline_summary.get("feature_count", len(FEATURE_COLUMNS)))
    selected_feature_count = int(selection_summary.get("feature_count_after", len(selected_features)))
    baseline_model_name = f"Baseline OLS ({baseline_feature_count} features)"
    selected_model_name = f"Selected OLS ({selected_feature_count} features)"

    pred_col = f"predicted_{TARGET}"

    def regression_metrics(name: str, prediction: np.ndarray, feature_count: int) -> dict:
        return {
            "model": name,
            "feature_count": feature_count,
            "MAE": float(mean_absolute_error(actual, prediction)),
            "RMSE": float(np.sqrt(mean_squared_error(actual, prediction))),
            "R2": float(r2_score(actual, prediction)),
        }

    metrics = [
        regression_metrics(
            baseline_model_name,
            baseline_predictions[pred_col].to_numpy(),
            baseline_feature_count,
        ),
        regression_metrics(
            selected_model_name,
            selected_predictions[pred_col].to_numpy(),
            selected_feature_count,
        ),
    ]
    metrics_table = pd.DataFrame(metrics)
    metrics_table.to_csv(tables_dir / "evaluation_metrics.csv", index=False)

    # 僅以訓練集 fit statsmodels OLS；測試集以 get_prediction 評估區間
    x_train_sm = sm.add_constant(train_data[selected_features], has_constant="add")
    x_test_sm = sm.add_constant(test_data[selected_features], has_constant="add")
    ols_result = sm.OLS(train_data[TARGET], x_train_sm).fit()
    prediction_frame = ols_result.get_prediction(x_test_sm).summary_frame(alpha=0.05)

    interval_table = pd.DataFrame(
        {
            "test_row": np.arange(len(test_data)),
            f"actual_{TARGET}": actual,
            "predicted_mean": prediction_frame["mean"].to_numpy(),
            "mean_ci_lower_95": prediction_frame["mean_ci_lower"].to_numpy(),
            "mean_ci_upper_95": prediction_frame["mean_ci_upper"].to_numpy(),
            "prediction_interval_lower_95": prediction_frame["obs_ci_lower"].to_numpy(),
            "prediction_interval_upper_95": prediction_frame["obs_ci_upper"].to_numpy(),
        }
    )
    interval_table["inside_prediction_interval"] = (
        interval_table[f"actual_{TARGET}"] >= interval_table["prediction_interval_lower_95"]
    ) & (
        interval_table[f"actual_{TARGET}"] <= interval_table["prediction_interval_upper_95"]
    )
    interval_table.to_csv(tables_dir / "selected_model_prediction_intervals.csv", index=False)

    residuals = ols_result.resid
    jb_stat, jb_pvalue, skewness, kurtosis = jarque_bera(residuals)
    bp_lm_stat, bp_lm_pvalue, bp_f_stat, bp_f_pvalue = het_breuschpagan(
        residuals, ols_result.model.exog
    )
    influence = ols_result.get_influence()
    cooks_distance = influence.cooks_distance[0]

    diagnostics = {
        "evaluated_model": selected_model_name,
        "interval_type": "95% prediction interval for an individual future observation",
        "prediction_interval_alpha": 0.05,
        "prediction_interval_test_coverage": float(
            interval_table["inside_prediction_interval"].mean()
        ),
        "prediction_interval_mean_width": float(
            (
                interval_table["prediction_interval_upper_95"]
                - interval_table["prediction_interval_lower_95"]
            ).mean()
        ),
        "jarque_bera_statistic": float(jb_stat),
        "jarque_bera_pvalue": float(jb_pvalue),
        "residual_skewness": float(skewness),
        "residual_kurtosis": float(kurtosis),
        "breusch_pagan_lm_statistic": float(bp_lm_stat),
        "breusch_pagan_lm_pvalue": float(bp_lm_pvalue),
        "breusch_pagan_f_statistic": float(bp_f_stat),
        "breusch_pagan_f_pvalue": float(bp_f_pvalue),
        "durbin_watson_statistic": float(durbin_watson(residuals)),
        "max_cooks_distance": float(cooks_distance.max()),
        "observations_above_cooks_4_over_n": int(
            (cooks_distance > 4 / len(train_data)).sum()
        ),
        "train_observation_count": int(len(train_data)),
    }
    (tables_dir / "residual_diagnostics.json").write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # 1. 實際值 vs 預測值對比散布圖
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharex=True, sharey=True)
    prediction_sets = [
        (baseline_model_name, baseline_predictions[pred_col]),
        (selected_model_name, selected_predictions[pred_col]),
    ]
    lower = min(actual.min(), *(prediction.min() for _, prediction in prediction_sets)) - 0.02
    upper = max(actual.max(), *(prediction.max() for _, prediction in prediction_sets)) + 0.02
    for ax, (title, prediction) in zip(axes, prediction_sets):
        ax.scatter(actual, prediction, alpha=0.3, color="#0A9396", s=15, edgecolor="none")
        ax.plot([lower, upper], [lower, upper], linestyle="--", color="#9B2226", linewidth=1.5, label="Ideal y = y_hat")
        ax.set(title=title, xlabel=f"Actual {TARGET}", ylabel=f"Predicted {TARGET}")
        ax.set_xlim(lower, upper)
        ax.set_ylim(lower, upper)
        ax.legend()
    fig.suptitle(f"Actual vs. Predicted {TARGET} on the Independent Test Set", fontsize=13)
    fig.tight_layout()
    fig.savefig(figures_dir / "actual_vs_predicted.png", dpi=160)
    plt.close(fig)

    # 2. 95% 預測區間圖（抽樣 200 點排序可視化，兼顧圖表清晰度）
    ordered = interval_table.sample(n=min(200, len(interval_table)), random_state=42).sort_values("predicted_mean").reset_index(drop=True)
    x_position = np.arange(len(ordered))
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.fill_between(
        x_position,
        ordered["prediction_interval_lower_95"].to_numpy(),
        ordered["prediction_interval_upper_95"].to_numpy(),
        color="#94D2BD",
        alpha=0.5,
        label="95% prediction interval (individual)",
    )
    ax.plot(
        x_position,
        ordered["predicted_mean"].to_numpy(),
        color="#005F73",
        linewidth=2,
        label="Predicted mean",
    )
    ax.scatter(
        x_position,
        ordered[f"actual_{TARGET}"].to_numpy(),
        color="#AE2012",
        s=18,
        alpha=0.75,
        label=f"Actual {TARGET}",
    )
    ax.set(
        title=f"{selected_model_name}: 95% Individual Prediction Intervals on Test Sample",
        xlabel="Observations (sorted by predicted value)",
        ylabel=TARGET,
    )
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(figures_dir / "selected_model_95_prediction_intervals.png", dpi=160)
    plt.close(fig)

    # 3. 殘差診斷圖
    fitted = ols_result.fittedvalues
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    sns.histplot(residuals, kde=True, color="#0A9396", bins=30, ax=axes[0])
    axes[0].set(title="Residual Distribution", xlabel="Residuals")

    sm.qqplot(residuals, line="45", fit=True, ax=axes[1])
    axes[1].set(title="Normal Q-Q Plot of Residuals")

    # 殘差 vs 擬合值散布圖取樣顯示以避免密集遮蔽
    sample_indices = np.random.RandomState(42).choice(len(fitted), size=min(2000, len(fitted)), replace=False)
    axes[2].scatter(fitted.iloc[sample_indices], residuals.iloc[sample_indices], alpha=0.3, color="#0A9396", s=10)
    axes[2].axhline(0, color="#9B2226", linestyle="--")
    axes[2].set(title="Residuals vs Fitted Values", xlabel="Fitted Values", ylabel="Residuals")

    fig.suptitle(f"{selected_model_name} Residual Diagnostics", fontsize=13)
    fig.tight_layout()
    fig.savefig(figures_dir / "selected_model_residual_diagnostics.png", dpi=160)
    plt.close(fig)

    print(json.dumps({"evaluation": metrics, "diagnostics": diagnostics}, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="AIoT HW2 Flood Prediction Multiple Linear Regression")
    parser.add_argument("--data-path", type=Path, default=Path("data/raw/train.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    args = parser.parse_args()

    data = load_data(args.data_path)
    save_data_understanding(data, args.output_dir)
    train_data, test_data = prepare_data(data, args.processed_dir, args.output_dir)
    train_baseline_model(train_data, test_data, args.output_dir)
    select_features_and_refit(train_data, test_data, args.output_dir)
    evaluate_models(train_data, test_data, args.output_dir)


if __name__ == "__main__":
    main()
