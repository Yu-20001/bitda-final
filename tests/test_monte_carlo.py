import numpy as np
import pytest

from amm_sim.monte_carlo import generate_gbm_paths, summarize_monte_carlo


def test_gbm_paths_are_deterministic_and_include_initial_price():
    first = generate_gbm_paths(0.6, days=30, paths=100, seed=7)
    second = generate_gbm_paths(0.6, days=30, paths=100, seed=7)

    assert first.shape == (100, 31)
    assert np.array_equal(first, second)
    assert np.all(first[:, 0] == 1.0)


def test_zero_volatility_paths_remain_at_one():
    generated = generate_gbm_paths(0.0, days=30, paths=20, seed=7)

    assert np.all(generated == 1.0)


def test_zero_volatility_summary_has_no_il_or_range_exits():
    summary = summarize_monte_carlo(
        annual_volatilities=[0.0],
        days=30,
        paths=100,
        seed=7,
        daily_volume_fraction=0.5,
        v3_ranges={
            "narrow": [0.95, 1.05],
            "medium": [0.80, 1.20],
            "wide": [0.50, 2.00],
        },
        weighted_pool_weights={"50_50": [0.5, 0.5], "80_20": [0.8, 0.2]},
    )

    assert len(summary) == 6
    assert summary["mean_impermanent_loss"].abs().max() == pytest.approx(0)
    assert summary["underperformance_probability"].max() == pytest.approx(0)
    assert summary["ever_exit_probability"].max() == pytest.approx(0)
    assert summary["mean_in_range_fraction"].min() == pytest.approx(1)


def test_v3_exit_probability_does_not_decrease_with_volatility():
    summary = summarize_monte_carlo(
        annual_volatilities=[0.2, 0.6, 1.0],
        days=30,
        paths=2_000,
        seed=7,
        daily_volume_fraction=0.5,
        v3_ranges={
            "narrow": [0.95, 1.05],
            "medium": [0.80, 1.20],
            "wide": [0.50, 2.00],
        },
        weighted_pool_weights={"50_50": [0.5, 0.5], "80_20": [0.8, 0.2]},
    )

    required = {
        "model",
        "configuration",
        "annual_volatility",
        "paths",
        "mean_terminal_price",
        "mean_impermanent_loss",
        "mean_fee_return",
        "mean_absolute_lp_return",
        "median_absolute_lp_return",
        "p05_absolute_lp_return",
        "mean_excess_return_vs_hold",
        "median_excess_return_vs_hold",
        "p05_excess_return_vs_hold",
        "underperformance_probability",
        "ever_exit_probability",
        "mean_in_range_fraction",
    }
    assert required.issubset(summary.columns)
    assert len(summary) == 18
    assert not summary.isna().any().any()

    v3 = summary[summary["model"] == "Uniswap V3"]
    for _, group in v3.groupby("configuration"):
        exits = group.sort_values("annual_volatility")["ever_exit_probability"]
        assert exits.is_monotonic_increasing
