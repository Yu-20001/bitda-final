from dataclasses import dataclass
from math import sqrt

from .common import SwapResult, make_swap_result


@dataclass(frozen=True)
class UniswapV3Position:
    liquidity: float
    initial_price: float
    lower_price: float
    upper_price: float
    fee_rate: float = 0.003

    @classmethod
    def from_capital(
        cls,
        capital: float,
        initial_price: float,
        lower_price: float,
        upper_price: float,
        fee_rate: float = 0.003,
    ) -> "UniswapV3Position":
        unit = cls(1.0, initial_price, lower_price, upper_price, fee_rate)
        amount_x, amount_y = unit.amounts(initial_price)
        liquidity = capital / (amount_x * initial_price + amount_y)
        return cls(liquidity, initial_price, lower_price, upper_price, fee_rate)

    def amounts(self, price: float) -> tuple[float, float]:
        root_p = sqrt(price)
        root_a = sqrt(self.lower_price)
        root_b = sqrt(self.upper_price)
        if price <= self.lower_price:
            return self.liquidity * (1 / root_a - 1 / root_b), 0.0
        if price >= self.upper_price:
            return 0.0, self.liquidity * (root_b - root_a)
        amount_x = self.liquidity * (1 / root_p - 1 / root_b)
        amount_y = self.liquidity * (root_p - root_a)
        return amount_x, amount_y

    def position_value(self, external_price: float) -> float:
        amount_x, amount_y = self.amounts(external_price)
        return amount_x * external_price + amount_y

    def quote_x_for_y(self, gross_input: float) -> SwapResult:
        net_input = gross_input * (1 - self.fee_rate)
        root_p = sqrt(self.initial_price)
        root_a = sqrt(self.lower_price)
        root_next = self.liquidity * root_p / (self.liquidity + net_input * root_p)
        if root_next < root_a:
            raise ValueError("exact input exceeds fixed-range capacity")
        output = self.liquidity * (root_p - root_next)
        return make_swap_result(
            gross_input,
            self.fee_rate,
            output,
            self.initial_price,
            root_next**2,
        )

    def path_availability(self, terminal_price: float) -> float:
        start = self.initial_price
        if self.lower_price <= terminal_price <= self.upper_price:
            return 1.0
        boundary = self.upper_price if terminal_price > self.upper_price else self.lower_price
        return abs(boundary - start) / abs(terminal_price - start)
