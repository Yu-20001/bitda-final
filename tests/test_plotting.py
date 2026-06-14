from pathlib import Path

from amm_sim.experiments import generate_all
from amm_sim.plotting import generate_figures


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
