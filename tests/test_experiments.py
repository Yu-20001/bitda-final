from pathlib import Path

from amm_sim.experiments import generate_all, load_config


def test_approved_configuration_is_loaded():
    config = load_config(Path("config/scenarios.yaml"))

    assert config["stableswap_amplifications"] == [10, 100, 1000]
    assert config["weighted_pool_weights"]["80_20"] == [0.8, 0.2]
    assert len(config["v3_ranges"]) == 3


def test_generate_all_has_expected_scenario_counts_and_columns(tmp_path):
    frames = generate_all(Path("config/scenarios.yaml"), tmp_path)

    assert len(frames["slippage"]) == 189
    assert len(frames["impermanent_loss"]) == 42
    assert len(frames["lp_return"]) == 126
    assert {"model", "configuration", "tvl", "trade_fraction", "slippage"}.issubset(
        frames["slippage"].columns
    )
    assert {"terminal_price", "impermanent_loss"}.issubset(
        frames["impermanent_loss"].columns
    )
    assert {"fee_return", "net_return"}.issubset(frames["lp_return"].columns)
    assert (tmp_path / "slippage.csv").exists()
    assert (tmp_path / "impermanent_loss.csv").exists()
    assert (tmp_path / "lp_return.csv").exists()


def test_generation_is_deterministic(tmp_path):
    first = generate_all(Path("config/scenarios.yaml"), tmp_path / "first")
    second = generate_all(Path("config/scenarios.yaml"), tmp_path / "second")

    assert first["slippage"].equals(second["slippage"])
    assert first["lp_return"].equals(second["lp_return"])
