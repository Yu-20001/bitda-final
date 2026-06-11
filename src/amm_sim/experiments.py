from pathlib import Path

import pandas as pd
import yaml

from .metrics import fee_return, impermanent_loss, lp_net_return
from .stableswap import StableSwapPool
from .uniswap_v2 import UniswapV2Pool
from .uniswap_v3 import UniswapV3Position
from .weighted_pool import WeightedPool


def load_config(path: Path) -> dict:
    with path.open() as handle:
        return yaml.safe_load(handle)


def _model_configurations(config: dict, tvl: float):
    yield "Uniswap V2", "0.30% fee", UniswapV2Pool(tvl / 2, tvl / 2)
    for name, bounds in config["v3_ranges"].items():
        yield (
            "Uniswap V3",
            f"{name} [{bounds[0]:.2f}, {bounds[1]:.2f}]",
            UniswapV3Position.from_capital(tvl, 1.0, bounds[0], bounds[1]),
        )
    for amplification in config["stableswap_amplifications"]:
        yield (
            "Curve StableSwap",
            f"A={amplification}",
            StableSwapPool(tvl / 2, tvl / 2, amplification),
        )
    for name, weights in config["weighted_pool_weights"].items():
        yield (
            "Balancer Weighted",
            name.replace("_", "/"),
            WeightedPool(tvl * weights[0], tvl * weights[1], *weights),
        )


def _generate_slippage(config: dict) -> pd.DataFrame:
    rows = []
    for tvl in config["tvls"]:
        for model, configuration, pool in _model_configurations(config, tvl):
            for trade_fraction in config["trade_fractions"]:
                quote = pool.quote_x_for_y(tvl * trade_fraction)
                rows.append(
                    {
                        "model": model,
                        "configuration": configuration,
                        "tvl": tvl,
                        "trade_fraction": trade_fraction,
                        "gross_input": quote.gross_input,
                        "fee_paid": quote.fee,
                        "output": quote.output,
                        "execution_price": quote.execution_price,
                        "slippage": quote.slippage,
                    }
                )
    return pd.DataFrame(rows)


def _generate_il(config: dict) -> pd.DataFrame:
    rows = []
    tvl = config["analysis_tvl"]
    for model, configuration, pool in _model_configurations(config, tvl):
        changes = (
            config["stable_price_changes"]
            if model == "Curve StableSwap"
            else config["terminal_price_changes"]
        )
        for change in changes:
            terminal_price = 1 + change
            rows.append(
                {
                    "model": model,
                    "configuration": configuration,
                    "terminal_price": terminal_price,
                    "price_change": change,
                    "impermanent_loss": impermanent_loss(pool, terminal_price),
                }
            )
    return pd.DataFrame(rows)


def _generate_lp_return(config: dict, il_frame: pd.DataFrame) -> pd.DataFrame:
    fee_rates = {
        "Uniswap V2": 0.003,
        "Uniswap V3": 0.003,
        "Curve StableSwap": 0.0004,
        "Balancer Weighted": 0.003,
    }
    v3_ranges = {
        f"{name} [{bounds[0]:.2f}, {bounds[1]:.2f}]": bounds
        for name, bounds in config["v3_ranges"].items()
    }
    rows = []
    for record in il_frame.to_dict("records"):
        availability = 1.0
        if record["model"] == "Uniswap V3":
            bounds = v3_ranges[record["configuration"]]
            position = UniswapV3Position.from_capital(
                config["analysis_tvl"], 1.0, bounds[0], bounds[1]
            )
            availability = position.path_availability(record["terminal_price"])
        for volume_fraction in config["daily_volume_fractions"]:
            fees = fee_return(
                volume_fraction,
                fee_rates[record["model"]],
                config["days"],
            )
            rows.append(
                {
                    **record,
                    "daily_volume_fraction": volume_fraction,
                    "availability": availability,
                    "fee_return": fees * availability,
                    "net_return": lp_net_return(
                        record["impermanent_loss"], fees, availability
                    ),
                }
            )
    return pd.DataFrame(rows)


def generate_all(config_path: Path, output_dir: Path) -> dict[str, pd.DataFrame]:
    config = load_config(config_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    slippage = _generate_slippage(config)
    il_frame = _generate_il(config)
    lp_return = _generate_lp_return(config, il_frame)
    frames = {
        "slippage": slippage,
        "impermanent_loss": il_frame,
        "lp_return": lp_return,
    }
    for name, frame in frames.items():
        frame.to_csv(output_dir / f"{name}.csv", index=False)
    return frames
