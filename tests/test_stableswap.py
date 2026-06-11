import pytest

from amm_sim.stableswap import StableSwapPool


def test_stableswap_swap_preserves_invariant():
    pool = StableSwapPool(500_000, 500_000, amplification=100)
    before = pool.invariant
    result = pool.quote_x_for_y(10_000)
    after = pool.compute_invariant(pool.reserve_x + result.net_input, pool.reserve_y - result.output)

    assert result.output > 0
    assert after == pytest.approx(before, rel=1e-9)


def test_higher_amplification_reduces_near_parity_slippage():
    low = StableSwapPool(500_000, 500_000, amplification=10)
    high = StableSwapPool(500_000, 500_000, amplification=1000)

    assert high.quote_x_for_y(10_000).slippage < low.quote_x_for_y(10_000).slippage


def test_stableswap_position_value_is_initial_value_at_parity():
    pool = StableSwapPool(500_000, 500_000, amplification=100)

    assert pool.position_value(1.0) == pytest.approx(1_000_000)


def test_stableswap_position_loses_relative_to_hold_after_small_depeg():
    pool = StableSwapPool(500_000, 500_000, amplification=100)
    hold_value = 500_000 * 1.05 + 500_000

    assert pool.position_value(1.05) < hold_value
