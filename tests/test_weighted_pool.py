import pytest

from amm_sim.weighted_pool import WeightedPool


def test_50_50_weighted_pool_matches_constant_product_output():
    pool = WeightedPool(500_000, 500_000, 0.5, 0.5, fee_rate=0.003)

    result = pool.quote_x_for_y(10_000)

    expected = 500_000 * (1 - (500_000 / 509_970))
    assert pool.spot_price == pytest.approx(1.0)
    assert result.output == pytest.approx(expected)


def test_80_20_pool_has_weighted_spot_price_and_preserves_invariant():
    pool = WeightedPool(800_000, 200_000, 0.8, 0.2)
    result = pool.quote_x_for_y(10_000)

    assert pool.spot_price == pytest.approx(1.0)
    before = pool.invariant
    after = (pool.reserve_x + result.net_input) ** 0.8 * (pool.reserve_y - result.output) ** 0.2
    assert after == pytest.approx(before)


def test_weighted_position_value_at_unchanged_price_equals_initial_value():
    pool = WeightedPool(800_000, 200_000, 0.8, 0.2)

    assert pool.position_value(1.0) == pytest.approx(1_000_000)
