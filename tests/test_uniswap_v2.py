import pytest

from amm_sim.uniswap_v2 import UniswapV2Pool


def test_v2_spot_price_and_swap():
    pool = UniswapV2Pool(500_000, 500_000, fee_rate=0.003)

    result = pool.quote_x_for_y(10_000)

    assert pool.spot_price == pytest.approx(1.0)
    assert result.fee == pytest.approx(30.0)
    assert result.output == pytest.approx(500_000 - 250_000_000_000 / 509_970)
    assert result.slippage > 0


def test_v2_effective_swap_preserves_invariant():
    pool = UniswapV2Pool(500_000, 500_000)
    result = pool.quote_x_for_y(10_000)

    assert (pool.reserve_x + result.net_input) * (pool.reserve_y - result.output) == pytest.approx(pool.invariant)


def test_v2_position_value_at_unchanged_price_equals_initial_value():
    pool = UniswapV2Pool(500_000, 500_000)

    assert pool.position_value(1.0) == pytest.approx(1_000_000)
