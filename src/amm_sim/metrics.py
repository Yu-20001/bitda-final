from .uniswap_v3 import UniswapV3Position


def _initial_holdings(position) -> tuple[float, float]:
    if isinstance(position, UniswapV3Position):
        return position.amounts(position.initial_price)
    return position.reserve_x, position.reserve_y


def impermanent_loss(position, terminal_price: float) -> float:
    initial_x, initial_y = _initial_holdings(position)
    hold_value = initial_x * terminal_price + initial_y
    return position.position_value(terminal_price) / hold_value - 1


def fee_return(daily_volume_fraction: float, fee_rate: float, days: int = 30) -> float:
    return daily_volume_fraction * fee_rate * days


def lp_net_return(
    impermanent_loss_value: float,
    fee_return_value: float,
    availability: float = 1.0,
) -> float:
    return impermanent_loss_value + fee_return_value * availability
