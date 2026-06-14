import pytest

from amm_sim.uniswap_v3 import UniswapV3Position


def test_v3_position_is_normalized_to_requested_capital():
    position = UniswapV3Position.from_capital(1_000_000, 1.0, 0.8, 1.2)
    amount_x, amount_y = position.amounts(1.0)

    assert amount_x + amount_y == pytest.approx(1_000_000)


def test_v3_inventory_changes_across_range():
    position = UniswapV3Position.from_capital(1_000_000, 1.0, 0.8, 1.2)

    below = position.amounts(0.7)
    inside = position.amounts(1.0)
    above = position.amounts(1.3)

    assert below[0] > 0 and below[1] == 0
    assert inside[0] > 0 and inside[1] > 0
    assert above[0] == 0 and above[1] > 0


def test_v3_swap_is_positive_and_cannot_cross_lower_bound():
    position = UniswapV3Position.from_capital(1_000_000, 1.0, 0.95, 1.05)

    result = position.quote_x_for_y(10_000)

    assert 0 < result.output
    assert result.terminal_price >= 0.95


def test_v3_rejects_exact_input_that_exceeds_range_capacity():
    position = UniswapV3Position.from_capital(1_000_000, 1.0, 0.95, 1.05)

    with pytest.raises(ValueError, match="exceeds fixed-range capacity"):
        position.quote_x_for_y(600_000)


def test_v3_path_availability_is_full_inside_and_partial_outside():
    position = UniswapV3Position.from_capital(1_000_000, 1.0, 0.8, 1.2)

    assert position.path_availability(1.1) == pytest.approx(1.0)
    assert 0 < position.path_availability(1.4) < 1
