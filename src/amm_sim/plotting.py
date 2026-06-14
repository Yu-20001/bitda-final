from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


def _setup() -> None:
    plt.rcParams.update(
        {
            "figure.figsize": (7.0, 4.2),
            "font.size": 9,
            "axes.grid": True,
            "grid.alpha": 0.25,
            "legend.fontsize": 7,
            "savefig.bbox": "tight",
        }
    )


def _label(row) -> str:
    return f"{row['model']} | {row['configuration']}"


def _save(path: Path) -> None:
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def generate_figures(frames: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _setup()

    slippage = frames["slippage"].copy()
    slippage["label"] = slippage.apply(_label, axis=1)

    selected = slippage[slippage["tvl"] == 1_000_000]
    for label, group in selected.groupby("label", sort=False):
        plt.plot(group["trade_fraction"], group["slippage"], marker="o", label=label)
    plt.xlabel("Trade input / TVL")
    plt.ylabel("Slippage")
    plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.legend(ncol=2)
    _save(output_dir / "slippage_comparison.pdf")

    v2 = slippage[slippage["model"] == "Uniswap V2"]
    for tvl, group in v2.groupby("tvl"):
        plt.plot(group["gross_input"], group["slippage"], marker="o", label=f"TVL ${tvl:,.0f}")
    plt.xlabel("Absolute trade input (USD-equivalent)")
    plt.ylabel("Slippage")
    plt.xscale("log")
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.legend()
    _save(output_dir / "liquidity_effect.pdf")

    stable = selected[selected["model"] == "Curve StableSwap"]
    for label, group in stable.groupby("label", sort=False):
        plt.plot(group["trade_fraction"], group["slippage"], marker="o", label=label)
    plt.xlabel("Trade input / TVL")
    plt.ylabel("Slippage")
    plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.legend()
    _save(output_dir / "stableswap_amplification.pdf")

    il_frame = frames["impermanent_loss"].copy()
    il_frame["label"] = il_frame.apply(_label, axis=1)
    for label, group in il_frame.groupby("label", sort=False):
        plt.plot(group["price_change"], group["impermanent_loss"], marker="o", label=label)
    plt.xlabel("Terminal price change")
    plt.ylabel("Impermanent loss")
    plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.legend(ncol=2)
    _save(output_dir / "impermanent_loss.pdf")

    returns = frames["lp_return"]
    returns = returns[returns["daily_volume_fraction"] == 0.5].copy()
    returns["label"] = returns.apply(_label, axis=1)
    for label, group in returns.groupby("label", sort=False):
        plt.plot(
            group["price_change"],
            group["excess_return_vs_hold"],
            marker="o",
            label=label,
        )
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xlabel("Terminal price change")
    plt.ylabel("30-day LP excess return vs HODL")
    plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.legend(ncol=2)
    _save(output_dir / "lp_return.pdf")

    monte_carlo = frames["monte_carlo_summary"].copy()
    monte_carlo["label"] = monte_carlo.apply(_label, axis=1)
    for label, group in monte_carlo.groupby("label", sort=False):
        group = group.sort_values("annual_volatility")
        plt.plot(
            group["annual_volatility"],
            group["mean_excess_return_vs_hold"],
            marker="o",
            label=f"{label} mean",
        )
        plt.plot(
            group["annual_volatility"],
            group["p05_excess_return_vs_hold"],
            linestyle="--",
            alpha=0.65,
            label=f"{label} 5th pct.",
        )
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xlabel("Annualized volatility")
    plt.ylabel("30-day LP excess return vs HODL")
    plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.legend(ncol=2)
    _save(output_dir / "monte_carlo_returns.pdf")

    v3 = monte_carlo[monte_carlo["model"] == "Uniswap V3"]
    for label, group in v3.groupby("label", sort=False):
        group = group.sort_values("annual_volatility")
        plt.plot(
            group["annual_volatility"],
            group["ever_exit_probability"],
            marker="o",
            label=label,
        )
    plt.xlabel("Annualized volatility")
    plt.ylabel("Probability of leaving range")
    plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.legend()
    _save(output_dir / "v3_range_risk.pdf")
