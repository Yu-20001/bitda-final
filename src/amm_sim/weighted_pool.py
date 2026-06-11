from dataclasses import dataclass

from .common import SwapResult, make_swap_result


@dataclass(frozen=True)
class WeightedPool:
    reserve_x: float
    reserve_y: float
    weight_x: float
    weight_y: float
    fee_rate: float = 0.003

    @property
    def invariant(self) -> float:
        return self.reserve_x**self.weight_x * self.reserve_y**self.weight_y

    @property
    def spot_price(self) -> float:
        return self.reserve_y * self.weight_x / (self.reserve_x * self.weight_y)

    def quote_x_for_y(self, gross_input: float) -> SwapResult:
        net_input = gross_input * (1 - self.fee_rate)
        ratio = self.reserve_x / (self.reserve_x + net_input)
        output = self.reserve_y * (1 - ratio ** (self.weight_x / self.weight_y))
        return make_swap_result(gross_input, self.fee_rate, output, self.spot_price)

    def position_value(self, external_price: float) -> float:
        ratio = external_price * self.weight_y / self.weight_x
        x = (self.invariant / ratio**self.weight_y) ** (1 / (self.weight_x + self.weight_y))
        y = ratio * x
        return x * external_price + y
