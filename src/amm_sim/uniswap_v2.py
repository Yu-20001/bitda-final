from dataclasses import dataclass
from math import sqrt

from .common import SwapResult, make_swap_result


@dataclass(frozen=True)
class UniswapV2Pool:
    reserve_x: float
    reserve_y: float
    fee_rate: float = 0.003

    @property
    def invariant(self) -> float:
        return self.reserve_x * self.reserve_y

    @property
    def spot_price(self) -> float:
        return self.reserve_y / self.reserve_x

    def quote_x_for_y(self, gross_input: float) -> SwapResult:
        net_input = gross_input * (1 - self.fee_rate)
        output = self.reserve_y - self.invariant / (self.reserve_x + net_input)
        return make_swap_result(gross_input, self.fee_rate, output, self.spot_price)

    def position_value(self, external_price: float) -> float:
        x = sqrt(self.invariant / external_price)
        y = sqrt(self.invariant * external_price)
        return x * external_price + y
