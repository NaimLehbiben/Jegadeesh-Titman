from typing import Optional
import numpy as np
from scipy.stats import norm
from src.pricing.base.option_base import OptionBase
from utils.type import OptionType


class VanillaOption(OptionBase):
    def __init__(
        self,
        spot_price: float,
        strike_price: float,
        maturity: float,
        rate: float,
        volatility: float,
        option_type: OptionType,
        dividend: Optional[float] = None,
    ) -> None:
        super().__init__(
            spot_price, strike_price, maturity, rate, volatility, option_type, dividend
        )

    def compute_price(self):
        if self._option_type == "call":
            return self._spot_price * norm.cdf(self._d1) - self._strike_price * np.exp(
                -(self._rate-self._dividend) * self._maturity
            ) * norm.cdf(self._d2)
        elif self._option_type == "put":
            return self._strike_price * np.exp(
                -(self._rate-self._dividend) * self._maturity
            ) * norm.cdf(-self._d2) - self._spot_price * norm.cdf(-self._d1)
        else:
            raise ValueError("Option type not supported. Use 'call' or 'put'.")

    def compute_delta(self):
        d1 = self._d1
        if self._option_type == "call":
            delta = norm.cdf(d1)
        elif self._option_type == "put":
            delta = norm.cdf(d1) - 1
        else:
            raise ValueError("Option type not supported. Use 'call' or 'put'.")
        return delta

    def compute_gamma(self):
        d1 = self._d1
        gamma = norm.pdf(d1) / (
            self._spot_price
            * self._volatility
            * np.sqrt(self._maturity)
        )
        return gamma

    def compute_theta(self):
        d1 = self._d1
        d2 = self._d2
        if self._option_type == "call":
            theta = (
                -self._spot_price * norm.pdf(d1) * self._volatility
            ) / (2 * np.sqrt(self._maturity)) - self._rate * self._strike_price * np.exp(
                -(self._rate-self._dividend) * self._maturity
            ) * norm.cdf(
                d2
            )
        elif self._option_type == "put":
            theta = (
                -self._spot_price * norm.pdf(d1) * self._volatility
            ) / (2 * np.sqrt(self._maturity)) + self._rate * self._strike_price * np.exp(
                -(self._rate-self._dividend) * self._maturity
            ) * norm.cdf(
                -d2
            )
        else:
            raise ValueError("Option type not supported. Use 'call' or 'put'.")
        return theta

    def compute_vega(self):
        d1 = self._d1
        vega = (
            self._spot_price
            * np.sqrt(self._maturity)
            * norm.pdf(d1)
            / 100
        )
        return vega

    def compute_rho(self):
        d2 = self._d2
        if self._option_type == "call":
            rho = (
                self._strike_price
                * self._maturity
                * np.exp(
                    -(self._rate-self._dividend)
                    * self._maturity
                )
                * norm.cdf(d2)
                / 100
            )
        elif self._option_type == "put":
            rho = (
                -self._strike_price
                * self._maturity
                * np.exp(
                    -(self._rate - self._dividend)
                    * self._maturity
                )
                * norm.cdf(-d2)
                / 100
            )
        else:
            raise ValueError("Option type not supported. Use 'call' or 'put'.")
        return rho

    def compute_greeks(self):
        return {
            "delta": self.compute_delta(),
            "gamma": self.compute_gamma(),
            "theta": self.compute_theta(),
            "vega": self.compute_vega(),
            "rho": self.compute_rho(),
        }