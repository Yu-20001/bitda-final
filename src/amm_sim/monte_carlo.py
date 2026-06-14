from math import sqrt

import numpy as np
import pandas as pd

from .metrics import (
    absolute_lp_return,
    excess_return_vs_hold,
    fee_return,
    impermanent_loss,
)
from .uniswap_v2 import UniswapV2Pool
from .uniswap_v3 import UniswapV3Position
from .weighted_pool import WeightedPool


def generate_gbm_paths(
    annual_volatility: float,
    days: int,
    paths: int,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    daily_volatility = annual_volatility / sqrt(365)
    shocks = rng.standard_normal((paths, days))
    log_returns = -0.5 * daily_volatility**2 + daily_volatility * shocks
    prices = np.exp(np.cumsum(log_returns, axis=1))
    return np.column_stack((np.ones(paths), prices))


def _configurations(v3_ranges: dict, weighted_pool_weights: dict):
    yield "Uniswap V2", "0.30% fee", UniswapV2Pool(0.5, 0.5)
    for name, bounds in v3_ranges.items():
        yield (
            "Uniswap V3",
            f"{name} [{bounds[0]:.2f}, {bounds[1]:.2f}]",
            UniswapV3Position.from_capital(1.0, 1.0, bounds[0], bounds[1]),
        )
    for name, weights in weighted_pool_weights.items():
        yield (
            "Balancer Weighted",
            name.replace("_", "/"),
            WeightedPool(weights[0], weights[1], *weights),
        )


def summarize_monte_carlo(
    annual_volatilities: list[float],
    days: int,
    paths: int,
    seed: int,
    daily_volume_fraction: float,
    v3_ranges: dict,
    weighted_pool_weights: dict,
) -> pd.DataFrame:
    rows = []
    gross_fee_return = fee_return(daily_volume_fraction, 0.003, days)
    for annual_volatility in annual_volatilities:
        price_paths = generate_gbm_paths(annual_volatility, days, paths, seed)
        terminal_prices = price_paths[:, -1]
        for model, configuration, position in _configurations(
            v3_ranges, weighted_pool_weights
        ):
            il_values = np.fromiter(
                (impermanent_loss(position, price) for price in terminal_prices),
                dtype=float,
                count=paths,
            )
            if isinstance(position, UniswapV3Position):
                observed = price_paths[:, 1:]
                in_range = (observed >= position.lower_price) & (
                    observed <= position.upper_price
                )
                availability = in_range.mean(axis=1)
                ever_exit = (~in_range).any(axis=1)
            else:
                availability = np.ones(paths)
                ever_exit = np.zeros(paths, dtype=bool)
            fee_values = gross_fee_return * availability
            absolute_returns = np.fromiter(
                (
                    absolute_lp_return(position, price, fee_value)
                    for price, fee_value in zip(terminal_prices, fee_values)
                ),
                dtype=float,
                count=paths,
            )
            excess_returns = np.fromiter(
                (
                    excess_return_vs_hold(position, price, fee_value)
                    for price, fee_value in zip(terminal_prices, fee_values)
                ),
                dtype=float,
                count=paths,
            )
            rows.append(
                {
                    "model": model,
                    "configuration": configuration,
                    "annual_volatility": annual_volatility,
                    "paths": paths,
                    "mean_terminal_price": terminal_prices.mean(),
                    "mean_impermanent_loss": il_values.mean(),
                    "mean_fee_return": fee_values.mean(),
                    "mean_absolute_lp_return": absolute_returns.mean(),
                    "median_absolute_lp_return": np.median(absolute_returns),
                    "p05_absolute_lp_return": np.quantile(absolute_returns, 0.05),
                    "mean_excess_return_vs_hold": excess_returns.mean(),
                    "median_excess_return_vs_hold": np.median(excess_returns),
                    "p05_excess_return_vs_hold": np.quantile(excess_returns, 0.05),
                    "underperformance_probability": (excess_returns < 0).mean(),
                    "ever_exit_probability": ever_exit.mean(),
                    "mean_in_range_fraction": availability.mean(),
                }
            )
    return pd.DataFrame(rows)
