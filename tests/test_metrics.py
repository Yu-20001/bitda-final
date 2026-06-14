from math import sqrt

import pytest

from amm_sim.metrics import (
    absolute_lp_return,
    excess_return_vs_hold,
    fee_return,
    impermanent_loss,
    terminal_hold_value,
)
from amm_sim.uniswap_v2 import UniswapV2Pool
from amm_sim.uniswap_v3 import UniswapV3Position
from amm_sim.weighted_pool import WeightedPool


def test_zero_price_change_has_zero_impermanent_loss():
    assert impermanent_loss(UniswapV2Pool(500_000, 500_000), 1.0) == pytest.approx(0)
    assert impermanent_loss(WeightedPool(800_000, 200_000, 0.8, 0.2), 1.0) == pytest.approx(0)


def test_v2_impermanent_loss_matches_known_formula():
    expected = 2 * sqrt(2) / 3 - 1

    assert impermanent_loss(UniswapV2Pool(500_000, 500_000), 2.0) == pytest.approx(expected)


def test_v3_impermanent_loss_uses_initial_fixed_range_inventory():
    position = UniswapV3Position.from_capital(1_000_000, 1.0, 0.8, 1.2)

    assert impermanent_loss(position, 1.0) == pytest.approx(0)
    assert impermanent_loss(position, 1.4) < 0


def test_deterministic_fee_return_fraction():
    fees = fee_return(daily_volume_fraction=0.5, fee_rate=0.003, days=30)

    assert fees == pytest.approx(0.045)


def test_absolute_and_hodl_relative_returns_use_consistent_denominators():
    position = UniswapV2Pool(500_000, 500_000)
    terminal_price = 0.5
    fee_value = 45_000

    assert terminal_hold_value(position, terminal_price) == pytest.approx(750_000)
    assert absolute_lp_return(position, terminal_price, fee_value) == pytest.approx(
        -0.24789321881345243
    )
    assert excess_return_vs_hold(position, terminal_price, fee_value) == pytest.approx(
        0.002809041582063354
    )
