"""7115056106 HW2：Red Wine Quality 多元線性回歸分析。

目前完成範圍：Step 2 Data Understanding、Step 3 Data Preparation、
Step 4 基準線性回歸模型、Step 5 Lasso 特徵選擇。
Step 6 模型評估與 95% 預測區間。
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
from sklearn.model_selection import GridSearchCV, StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson, jarque_bera


EXPECTED_COLUMNS = [
    "fixed acidity",
    "volatile acidity",
    "citric acid",
    "residual sugar",
    "chlorides",
    "free sulfur dioxide",
    "total sulfur dioxide",
    "density",
    "pH",
    "sulphates",
    "alcohol",
    "quality",
]
TARGET = "quality"


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

    summary = {
        "row_count": int(data.shape[0]),
        "column_count": int(data.shape[1]),
        "feature_count": int(data.shape[1] - 1),
        "target": TARGET,
        "column_names": data.columns.tolist(),
        "dtypes": {column: str(dtype) for column, dtype in data.dtypes.items()},
        "missing_value_count": int(data.isna().sum().sum()),
        "duplicate_row_count": int(data.duplicated().sum()),
        "target_min": int(data[TARGET].min()),
        "target_max": int(data[TARGET].max()),
        "target_mean": float(data[TARGET].mean()),
        "target_median": float(data[TARGET].median()),
    }
    (tables_dir / "data_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    data.describe().T.to_csv(tables_dir / "descriptive_statistics.csv", encoding="utf-8")
    pd.DataFrame(
        {
            "dtype": data.dtypes.astype(str),
            "missing_count": data.isna().sum(),
            "unique_count": data.nunique(dropna=False),
        }
    ).to_csv(tables_dir / "column_quality_summary.csv", encoding="utf-8")

    target_distribution = (
        data[TARGET]
        .value_counts(dropna=False)
        .sort_index()
        .rename_axis(TARGET)
        .reset_index(name="count")
    )
    target_distribution["proportion"] = target_distribution["count"] / len(data)
    target_distribution.to_csv(tables_dir / "target_distribution.csv", index=False)

    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=data, x=TARGET, color="#9B2226", ax=ax)
    ax.set(title="Red Wine Quality Distribution", xlabel="Quality score", ylabel="Count")
    fig.tight_layout()
    fig.savefig(figures_dir / "target_distribution.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 9))
    correlation = data.corr(numeric_only=True)
    sns.heatmap(
        correlation,
        cmap="vlag",
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=0.3,
        ax=ax,
    )
    ax.set_title("Pearson Correlation Matrix")
    fig.tight_layout()
    fig.savefig(figures_dir / "correlation_heatmap.png", dpi=160)
    plt.close(fig)

    features = [column for column in data.columns if column != TARGET]
    axes = data[features].hist(bins=25, figsize=(14, 10), color="#0A9396", edgecolor="white")
    for ax in axes.ravel():
        ax.set_ylabel("Count")
    plt.suptitle("Feature Distributions", y=1.01)
    plt.tight_layout()
    plt.savefig(figures_dir / "feature_distributions.png", dpi=160, bbox_inches="tight")
    plt.close("all")

    print(json.dumps(summary, ensure_ascii=False, indent=2))


def split_and_save_data(
    data: pd.DataFrame,
    processed_dir: Path,
    output_dir: Path,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """以完整列作為群組進行 80/20 分層切分，避免相同列跨集合。"""
    processed_dir.mkdir(parents=True, exist_ok=True)
    tables_dir = output_dir / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)

    # 完全相同的 11 個特徵與目標會得到相同 group id。
    groups = data.groupby(EXPECTED_COLUMNS, sort=False, dropna=False).ngroup()
    splitter = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=random_state)

    # 五個 fold 都符合同組不跨集合；選擇列數最接近 20% 且目標分布最接近全體者。
    overall_distribution = data[TARGET].value_counts(normalize=True).sort_index()
    candidates: list[tuple[float, int, list[int], list[int]]] = []
    for fold_number, (train_index, test_index) in enumerate(
        splitter.split(data.drop(columns=TARGET), data[TARGET], groups=groups), start=1
    ):
        test_distribution = (
            data.iloc[test_index][TARGET]
            .value_counts(normalize=True)
            .reindex(overall_distribution.index, fill_value=0)
        )
        size_error = abs(len(test_index) / len(data) - 0.20)
        distribution_error = float((test_distribution - overall_distribution).abs().max())
        candidates.append(
            (size_error + distribution_error, fold_number, train_index.tolist(), test_index.tolist())
        )

    _, selected_fold, train_index, test_index = min(candidates, key=lambda item: item[0])
    train_data = data.iloc[train_index].copy()
    test_data = data.iloc[test_index].copy()

    train_groups = set(groups.iloc[train_index])
    test_groups = set(groups.iloc[test_index])
    overlap = train_groups.intersection(test_groups)
    if overlap:
        raise RuntimeError(f"偵測到 {len(overlap)} 個群組跨越訓練集與測試集。")

    train_data.to_csv(processed_dir / "train.csv", index=False)
    test_data.to_csv(processed_dir / "test.csv", index=False)

    quality_values = sorted(int(value) for value in data[TARGET].unique())

    def counts(frame: pd.DataFrame) -> dict[str, int]:
        value_counts = frame[TARGET].value_counts()
        return {str(value): int(value_counts.get(value, 0)) for value in quality_values}

    def proportions(frame: pd.DataFrame) -> dict[str, float]:
        value_counts = frame[TARGET].value_counts(normalize=True)
        return {str(value): float(value_counts.get(value, 0)) for value in quality_values}

    summary = {
        "strategy": "StratifiedGroupKFold candidate fold closest to 20% and overall target distribution",
        "random_state": random_state,
        "n_splits": 5,
        "selected_fold": selected_fold,
        "group_definition": "all 11 features plus quality are identical",
        "original_rows": int(len(data)),
        "unique_complete_rows": int(data.drop_duplicates().shape[0]),
        "duplicate_rows_beyond_first": int(data.duplicated().sum()),
        "train_rows": int(len(train_data)),
        "test_rows": int(len(test_data)),
        "test_fraction": float(len(test_data) / len(data)),
        "train_unique_groups": int(len(train_groups)),
        "test_unique_groups": int(len(test_groups)),
        "group_overlap_count": int(len(overlap)),
        "missing_values_train": int(train_data.isna().sum().sum()),
        "missing_values_test": int(test_data.isna().sum().sum()),
        "target_counts": {
            "overall": counts(data),
            "train": counts(train_data),
            "test": counts(test_data),
        },
        "target_proportions": {
            "overall": proportions(data),
            "train": proportions(train_data),
            "test": proportions(test_data),
        },
    }
    (tables_dir / "split_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(json.dumps({"data_preparation": summary}, ensure_ascii=False, indent=2))
    return train_data, test_data


def fit_baseline_model(
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    output_dir: Path,
) -> None:
    """使用全部 11 個特徵訓練基準普通最小平方法模型。"""
    features = [column for column in EXPECTED_COLUMNS if column != TARGET]
    x_train = train_data[features]
    y_train = train_data[TARGET]
    x_test = test_data[features]
    y_test = test_data[TARGET]

    model = LinearRegression()
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    if not np.isfinite(predictions).all():
        raise RuntimeError("基準模型產生非有限數值預測。")

    tables_dir = output_dir / "tables"
    models_dir = output_dir / "models"
    tables_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(
        {
            "test_row": np.arange(len(test_data)),
            "actual_quality": y_test.to_numpy(),
            "predicted_quality": predictions,
            "residual": y_test.to_numpy() - predictions,
        }
    ).to_csv(tables_dir / "baseline_predictions.csv", index=False)

    coefficients = pd.DataFrame(
        {
            "feature": features,
            "coefficient": model.coef_,
        }
    )
    coefficients.to_csv(tables_dir / "baseline_coefficients.csv", index=False)

    model_summary = {
        "model": "sklearn.linear_model.LinearRegression",
        "fit_intercept": bool(model.fit_intercept),
        "features": features,
        "feature_count": len(features),
        "train_rows": int(len(train_data)),
        "test_rows": int(len(test_data)),
        "intercept": float(model.intercept_),
        "prediction_count": int(len(predictions)),
        "prediction_min": float(predictions.min()),
        "prediction_max": float(predictions.max()),
        "prediction_mean": float(predictions.mean()),
    }
    (tables_dir / "baseline_model_summary.json").write_text(
        json.dumps(model_summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    dump(model, models_dir / "baseline_linear_regression.joblib")

    print(json.dumps({"baseline_model": model_summary}, ensure_ascii=False, indent=2))


def select_features_and_refit(
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    output_dir: Path,
    random_state: int = 42,
) -> None:
    """用訓練集內的 group-aware CV Lasso 選特徵，再重建 OLS。"""
    features = [column for column in EXPECTED_COLUMNS if column != TARGET]
    x_train = train_data[features]
    y_train = train_data[TARGET]
    x_test = test_data[features]

    train_groups = train_data.groupby(EXPECTED_COLUMNS, sort=False, dropna=False).ngroup()
    cv_splitter = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=random_state)
    cv_splits = list(cv_splitter.split(x_train, y_train, groups=train_groups))

    selector_pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("lasso", Lasso(max_iter=100_000, tol=1e-8, random_state=random_state)),
        ]
    )
    alpha_grid = np.logspace(-4, 0, 81)
    search = GridSearchCV(
        selector_pipeline,
        param_grid={"lasso__alpha": alpha_grid},
        scoring="neg_root_mean_squared_error",
        cv=cv_splits,
        refit=False,
        n_jobs=1,
        return_train_score=False,
    )
    search.fit(x_train, y_train)

    cv_results = pd.DataFrame(search.cv_results_)
    cv_results["alpha"] = cv_results["param_lasso__alpha"].astype(float)
    cv_results["mean_cv_rmse"] = -cv_results["mean_test_score"]
    cv_results["std_cv_rmse"] = cv_results["std_test_score"]
    cv_results["se_cv_rmse"] = cv_results["std_cv_rmse"] / np.sqrt(len(cv_splits))

    minimum_index = cv_results["mean_cv_rmse"].idxmin()
    minimum_rmse = float(cv_results.loc[minimum_index, "mean_cv_rmse"])
    minimum_se = float(cv_results.loc[minimum_index, "se_cv_rmse"])
    one_se_threshold = minimum_rmse + minimum_se
    eligible = cv_results.loc[cv_results["mean_cv_rmse"] <= one_se_threshold]
    selected_alpha = float(eligible["alpha"].max())

    selector_pipeline.set_params(lasso__alpha=selected_alpha)
    selector_pipeline.fit(x_train, y_train)
    standardized_coefficients = selector_pipeline.named_steps["lasso"].coef_
    selected_features = [
        feature
        for feature, coefficient in zip(features, standardized_coefficients)
        if abs(coefficient) > 1e-8
    ]
    if not selected_features or len(selected_features) >= len(features):
        raise RuntimeError(
            f"Lasso 未產生有效的特徵子集：選出 {len(selected_features)}/{len(features)} 個。"
        )

    selected_model = LinearRegression()
    selected_model.fit(train_data[selected_features], y_train)
    selected_predictions = selected_model.predict(test_data[selected_features])
    if not np.isfinite(selected_predictions).all():
        raise RuntimeError("特徵選擇後模型產生非有限數值預測。")

    tables_dir = output_dir / "tables"
    models_dir = output_dir / "models"
    figures_dir = output_dir / "figures"
    tables_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    cv_results[
        ["alpha", "mean_cv_rmse", "std_cv_rmse", "se_cv_rmse", "rank_test_score"]
    ].sort_values("alpha").to_csv(tables_dir / "lasso_alpha_cv_results.csv", index=False)

    selection_table = pd.DataFrame(
        {
            "feature": features,
            "standardized_lasso_coefficient": standardized_coefficients,
            "selected": [feature in selected_features for feature in features],
        }
    )
    selection_table.to_csv(tables_dir / "feature_selection.csv", index=False)

    pd.DataFrame(
        {
            "test_row": np.arange(len(test_data)),
            "actual_quality": test_data[TARGET].to_numpy(),
            "predicted_quality": selected_predictions,
            "residual": test_data[TARGET].to_numpy() - selected_predictions,
        }
    ).to_csv(tables_dir / "selected_model_predictions.csv", index=False)

    pd.DataFrame(
        {"feature": selected_features, "coefficient": selected_model.coef_}
    ).to_csv(tables_dir / "selected_model_coefficients.csv", index=False)

    selection_summary = {
        "method": "StandardScaler + Lasso with stratified group 5-fold CV",
        "selection_rule": "largest alpha within one standard error of minimum CV RMSE",
        "random_state": random_state,
        "alpha_candidates": int(len(alpha_grid)),
        "minimum_cv_rmse": minimum_rmse,
        "one_se_threshold": one_se_threshold,
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

    fig, ax = plt.subplots(figsize=(9, 5))
    plot_data = selection_table.sort_values("standardized_lasso_coefficient")
    colors = ["#0A9396" if selected else "#B7B7B7" for selected in plot_data["selected"]]
    ax.barh(plot_data["feature"], plot_data["standardized_lasso_coefficient"], color=colors)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set(
        title=f"Lasso Feature Selection (alpha={selected_alpha:.5g})",
        xlabel="Coefficient after standardization",
        ylabel="Feature",
    )
    fig.tight_layout()
    fig.savefig(figures_dir / "lasso_feature_selection.png", dpi=160)
    plt.close(fig)

    print(json.dumps({"feature_selection": selection_summary}, ensure_ascii=False, indent=2))


def evaluate_models(
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    output_dir: Path,
) -> None:
    """在固定測試集比較模型，並建立精簡 OLS 的 95% 預測區間。"""
    tables_dir = output_dir / "tables"
    figures_dir = output_dir / "figures"
    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    baseline_predictions = pd.read_csv(tables_dir / "baseline_predictions.csv")
    selected_predictions = pd.read_csv(tables_dir / "selected_model_predictions.csv")
    selection_summary = json.loads(
        (tables_dir / "feature_selection_summary.json").read_text(encoding="utf-8")
    )
    selected_features = selection_summary["features_after"]
    actual = test_data[TARGET].to_numpy()

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
            "Baseline OLS (11 features)",
            baseline_predictions["predicted_quality"].to_numpy(),
            11,
        ),
        regression_metrics(
            "Selected OLS (4 features)",
            selected_predictions["predicted_quality"].to_numpy(),
            len(selected_features),
        ),
    ]
    metrics_table = pd.DataFrame(metrics)
    metrics_table.to_csv(tables_dir / "evaluation_metrics.csv", index=False)

    # 僅以訓練集 fit statsmodels OLS；測試集只傳入 get_prediction。
    x_train_sm = sm.add_constant(train_data[selected_features], has_constant="add")
    x_test_sm = sm.add_constant(test_data[selected_features], has_constant="add")
    ols_result = sm.OLS(train_data[TARGET], x_train_sm).fit()
    prediction_frame = ols_result.get_prediction(x_test_sm).summary_frame(alpha=0.05)
    interval_table = pd.DataFrame(
        {
            "test_row": np.arange(len(test_data)),
            "actual_quality": actual,
            "predicted_mean": prediction_frame["mean"].to_numpy(),
            "mean_ci_lower_95": prediction_frame["mean_ci_lower"].to_numpy(),
            "mean_ci_upper_95": prediction_frame["mean_ci_upper"].to_numpy(),
            "prediction_interval_lower_95": prediction_frame["obs_ci_lower"].to_numpy(),
            "prediction_interval_upper_95": prediction_frame["obs_ci_upper"].to_numpy(),
        }
    )
    interval_table["inside_prediction_interval"] = (
        interval_table["actual_quality"] >= interval_table["prediction_interval_lower_95"]
    ) & (
        interval_table["actual_quality"] <= interval_table["prediction_interval_upper_95"]
    )
    interval_table.to_csv(tables_dir / "selected_model_prediction_intervals.csv", index=False)

    residuals = ols_result.resid
    fitted = ols_result.fittedvalues
    jb_stat, jb_pvalue, skewness, kurtosis = jarque_bera(residuals)
    bp_lm_stat, bp_lm_pvalue, bp_f_stat, bp_f_pvalue = het_breuschpagan(
        residuals, ols_result.model.exog
    )
    influence = ols_result.get_influence()
    cooks_distance = influence.cooks_distance[0]
    diagnostics = {
        "evaluated_model": "Selected OLS (4 features)",
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

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharex=True, sharey=True)
    prediction_sets = [
        ("Baseline OLS (11 features)", baseline_predictions["predicted_quality"]),
        ("Selected OLS (4 features)", selected_predictions["predicted_quality"]),
    ]
    lower = min(actual.min(), *(prediction.min() for _, prediction in prediction_sets)) - 0.2
    upper = max(actual.max(), *(prediction.max() for _, prediction in prediction_sets)) + 0.2
    for ax, (title, prediction) in zip(axes, prediction_sets):
        ax.scatter(actual, prediction, alpha=0.55, color="#0A9396", edgecolor="none")
        ax.plot([lower, upper], [lower, upper], linestyle="--", color="#9B2226")
        ax.set(title=title, xlabel="Actual quality", ylabel="Predicted quality")
        ax.set_xlim(lower, upper)
        ax.set_ylim(lower, upper)
    fig.suptitle("Actual vs. Predicted Quality on the Fixed Test Set")
    fig.tight_layout()
    fig.savefig(figures_dir / "actual_vs_predicted.png", dpi=160)
    plt.close(fig)

    ordered = interval_table.sort_values("predicted_mean").reset_index(drop=True)
    x_position = np.arange(len(ordered))
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.fill_between(
        x_position,
        ordered["prediction_interval_lower_95"].to_numpy(),
        ordered["prediction_interval_upper_95"].to_numpy(),
        color="#94D2BD",
        alpha=0.5,
        label="95% prediction interval",
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
        ordered["actual_quality"].to_numpy(),
        color="#9B2226",
        s=14,
        alpha=0.65,
        label="Actual quality",
    )
    ax.set(
        title="Selected OLS: Test Predictions with 95% Prediction Intervals",
        xlabel="Test observations ordered by predicted mean",
        ylabel="Quality score",
    )
    ax.legend()
    fig.tight_layout()
    fig.savefig(figures_dir / "selected_model_95_prediction_intervals.png", dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    axes[0].scatter(fitted, residuals, alpha=0.5, color="#0A9396", edgecolor="none")
    axes[0].axhline(0, linestyle="--", color="#9B2226")
    axes[0].set(title="Residuals vs. Fitted", xlabel="Fitted value", ylabel="Residual")
    sm.qqplot(residuals, line="45", fit=True, ax=axes[1])
    axes[1].set_title("Normal Q-Q")
    axes[2].scatter(np.arange(len(cooks_distance)), cooks_distance, s=10, color="#EE9B00")
    axes[2].axhline(4 / len(train_data), linestyle="--", color="#9B2226", label="4/n")
    axes[2].set(title="Cook's Distance", xlabel="Training observation", ylabel="Cook's D")
    axes[2].legend()
    fig.suptitle("Selected OLS Residual Diagnostics")
    fig.tight_layout()
    fig.savefig(figures_dir / "selected_model_residual_diagnostics.png", dpi=160)
    plt.close(fig)

    print(json.dumps({"evaluation": metrics, "diagnostics": diagnostics}, ensure_ascii=False, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data",
        type=Path,
        default=Path("data/raw/winequality-red.csv"),
        help="Red Wine Quality CSV 路徑",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs"),
        help="分析輸出目錄",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=Path("data/processed"),
        help="訓練集與測試集輸出目錄",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = load_data(args.data)
    save_data_understanding(data, args.output_dir)
    train_data, test_data = split_and_save_data(data, args.processed_dir, args.output_dir)
    fit_baseline_model(train_data, test_data, args.output_dir)
    select_features_and_refit(train_data, test_data, args.output_dir)
    evaluate_models(train_data, test_data, args.output_dir)


if __name__ == "__main__":
    main()
