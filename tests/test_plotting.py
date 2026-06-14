from pathlib import Path

import matplotlib.pyplot as plt

from amm_sim.experiments import generate_all
from amm_sim.plotting import _new_figure, generate_figures


def test_new_figure_uses_distinct_single_and_double_column_profiles():
    single = _new_figure("single")
    assert tuple(single.get_size_inches()) == (4.4, 3.1)
    assert plt.rcParams["font.size"] == 10
    plt.close(single)

    double = _new_figure("double")
    assert tuple(double.get_size_inches()) == (7.4, 3.8)
    assert plt.rcParams["font.size"] == 10
    plt.close(double)


def test_generate_figures_creates_required_report_assets(tmp_path):
    frames = generate_all(Path("config/scenarios.yaml"), tmp_path / "data")
    figure_dir = tmp_path / "figures"

    generate_figures(frames, figure_dir)

    expected = {
        "slippage_comparison.pdf",
        "liquidity_effect.pdf",
        "stableswap_amplification.pdf",
        "impermanent_loss.pdf",
        "lp_return.pdf",
        "monte_carlo_returns.pdf",
        "v3_range_risk.pdf",
    }
    assert expected == {path.name for path in figure_dir.glob("*.pdf")}
    assert all((figure_dir / name).stat().st_size > 1_000 for name in expected)
