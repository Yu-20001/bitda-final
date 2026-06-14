from pathlib import Path

import pytest

from amm_sim.experiments import generate_all, load_config


def test_approved_configuration_is_loaded():
    config = load_config(Path("config/scenarios.yaml"))

    assert config["stableswap_amplifications"] == [10, 100, 1000]
    assert config["weighted_pool_weights"]["80_20"] == [0.8, 0.2]
    assert len(config["v3_ranges"]) == 3
    assert config["monte_carlo"] == {
        "annual_volatilities": [0.2, 0.6, 1.0],
        "paths": 10000,
        "seed": 20260611,
        "daily_volume_fraction": 0.5,
    }


def test_generate_all_has_expected_scenario_counts_and_columns(tmp_path):
    frames = generate_all(Path("config/scenarios.yaml"), tmp_path)

    assert len(frames["slippage"]) == 189
    assert len(frames["impermanent_loss"]) == 42
    assert len(frames["lp_return"]) == 126
    assert len(frames["monte_carlo_summary"]) == 18
    assert {
        "model",
        "configuration",
        "tvl",
        "trade_fraction",
        "gross_input",
        "fee_paid",
        "net_input",
        "output",
        "execution_price",
        "slippage",
    }.issubset(frames["slippage"].columns)
    assert {"terminal_price", "impermanent_loss"}.issubset(
        frames["impermanent_loss"].columns
    )
    assert {
        "fee_return",
        "fee_value",
        "absolute_lp_return",
        "excess_return_vs_hold",
    }.issubset(frames["lp_return"].columns)
    assert "net_return" not in frames["lp_return"].columns
    assert {
        "annual_volatility",
        "mean_absolute_lp_return",
        "mean_excess_return_vs_hold",
        "p05_excess_return_vs_hold",
        "underperformance_probability",
        "ever_exit_probability",
        "mean_in_range_fraction",
    }.issubset(frames["monte_carlo_summary"].columns)
    assert "loss_probability" not in frames["monte_carlo_summary"].columns
    assert not frames["monte_carlo_summary"].isna().any().any()
    assert (tmp_path / "slippage.csv").exists()
    assert (tmp_path / "impermanent_loss.csv").exists()
    assert (tmp_path / "lp_return.csv").exists()
    assert (tmp_path / "monte_carlo_summary.csv").exists()

    v2_down_50 = frames["lp_return"].query(
        "model == 'Uniswap V2' and price_change == -0.5 and daily_volume_fraction == 0.5"
    ).iloc[0]
    assert v2_down_50["absolute_lp_return"] == pytest.approx(-0.24789321881345243)
    assert v2_down_50["excess_return_vs_hold"] == pytest.approx(0.002809041582063354)


def test_generation_is_deterministic(tmp_path):
    first = generate_all(Path("config/scenarios.yaml"), tmp_path / "first")
    second = generate_all(Path("config/scenarios.yaml"), tmp_path / "second")

    assert first["slippage"].equals(second["slippage"])
    assert first["lp_return"].equals(second["lp_return"])
    assert first["monte_carlo_summary"].equals(second["monte_carlo_summary"])
