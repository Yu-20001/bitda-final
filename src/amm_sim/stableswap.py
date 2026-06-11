from dataclasses import dataclass

from scipy.optimize import minimize_scalar

from .common import SwapResult, make_swap_result


@dataclass(frozen=True)
class StableSwapPool:
    reserve_x: float
    reserve_y: float
    amplification: float
    fee_rate: float = 0.0004

    @property
    def invariant(self) -> float:
        return self.compute_invariant(self.reserve_x, self.reserve_y)

    @property
    def spot_price(self) -> float:
        epsilon = max(self.reserve_x, self.reserve_y) * 1e-8
        return self._output_without_fee(epsilon) / epsilon

    def compute_invariant(self, x: float, y: float) -> float:
        total = x + y
        if total == 0:
            return 0.0
        n = 2
        ann = self.amplification * n
        d = total
        for _ in range(255):
            d_product = d
            for balance in (x, y):
                d_product = d_product * d / (balance * n)
            previous = d
            d = (ann * total + d_product * n) * d / (
                (ann - 1) * d + (n + 1) * d_product
            )
            if abs(d - previous) <= 1e-12:
                break
        return d

    def _get_y(self, x: float, d: float) -> float:
        n = 2
        ann = self.amplification * n
        c = d * d / (x * n)
        c = c * d / (ann * n)
        b = x + d / ann
        y = d
        for _ in range(255):
            previous = y
            y = (y * y + c) / (2 * y + b - d)
            if abs(y - previous) <= 1e-12:
                break
        return y

    def _output_without_fee(self, net_input: float) -> float:
        new_y = self._get_y(self.reserve_x + net_input, self.invariant)
        return self.reserve_y - new_y

    def quote_x_for_y(self, gross_input: float) -> SwapResult:
        net_input = gross_input * (1 - self.fee_rate)
        output = self._output_without_fee(net_input)
        return make_swap_result(gross_input, self.fee_rate, output, self.spot_price)

    def position_value(self, external_price: float) -> float:
        if external_price == 1.0:
            return self.reserve_x + self.reserve_y
        d = self.invariant

        def value_at_x(x: float) -> float:
            return x * external_price + self._get_y(x, d)

        result = minimize_scalar(
            value_at_x,
            bounds=(d * 1e-6, d * (1 - 1e-6)),
            method="bounded",
        )
        return result.fun
