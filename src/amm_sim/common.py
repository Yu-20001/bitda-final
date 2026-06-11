from dataclasses import dataclass


@dataclass(frozen=True)
class SwapResult:
    gross_input: float
    fee: float
    net_input: float
    output: float
    spot_price: float
    execution_price: float
    slippage: float
    terminal_price: float | None = None


def make_swap_result(
    gross_input: float,
    fee_rate: float,
    output: float,
    spot_price: float,
    terminal_price: float | None = None,
) -> SwapResult:
    fee = gross_input * fee_rate
    net_input = gross_input - fee
    execution_price = output / gross_input
    slippage = 1 - execution_price / spot_price
    return SwapResult(
        gross_input,
        fee,
        net_input,
        output,
        spot_price,
        execution_price,
        slippage,
        terminal_price,
    )
