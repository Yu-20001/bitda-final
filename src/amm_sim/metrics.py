from .uniswap_v3 import UniswapV3Position


def _initial_holdings(position) -> tuple[float, float]:
    if isinstance(position, UniswapV3Position):
        return position.amounts(position.initial_price)
    return position.reserve_x, position.reserve_y


def _initial_price(position) -> float:
    if isinstance(position, UniswapV3Position):
        return position.initial_price
    return position.spot_price


def initial_position_value(position) -> float:
    initial_x, initial_y = _initial_holdings(position)
    return initial_x * _initial_price(position) + initial_y


def terminal_hold_value(position, terminal_price: float) -> float:
    initial_x, initial_y = _initial_holdings(position)
    return initial_x * terminal_price + initial_y


def impermanent_loss(position, terminal_price: float) -> float:
    return position.position_value(terminal_price) / terminal_hold_value(
        position, terminal_price
    ) - 1


def fee_return(daily_volume_fraction: float, fee_rate: float, days: int = 30) -> float:
    return daily_volume_fraction * fee_rate * days


def absolute_lp_return(
    position,
    terminal_price: float,
    fee_value: float,
) -> float:
    terminal_value = position.position_value(terminal_price) + fee_value
    return terminal_value / initial_position_value(position) - 1


def excess_return_vs_hold(
    position,
    terminal_price: float,
    fee_value: float,
) -> float:
    terminal_value = position.position_value(terminal_price) + fee_value
    return terminal_value / terminal_hold_value(position, terminal_price) - 1
