from math import sqrt

import pytest

from amm_sim.metrics import fee_return, impermanent_loss, lp_net_return
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


def test_deterministic_fee_and_net_return():
    fees = fee_return(daily_volume_fraction=0.5, fee_rate=0.003, days=30)

    assert fees == pytest.approx(0.045)
    assert lp_net_return(-0.02, fees, availability=0.5) == pytest.approx(0.0025)
