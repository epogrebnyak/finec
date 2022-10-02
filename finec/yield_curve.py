"""Получение параметров кривой бескупонной доходности и расчет доходности.

https://github.com/cmf-team/pricer/issues/3#issuecomment-1264697353

"""
#%%
from dataclasses import dataclass
import numpy as np
from finec.moex import Endpoint


#%%
a1 = 0
a2 = 0.6
k = 1.6


def a(n: int):
    if n == 1:
        return a1
    if n == 2:
        return a2
    return a(n - 1) + a(2) * k ** (n - 2)


def b(n: int):
    if n == 1:
        return a(2)
    else:
        return b(n - 1) * k


def s(t, params):
    res = 0
    for i in range(1, 9 + 1):
        g = params[f"g{i}"]
        res += g * np.exp(-((t - a(i)) ** 2) / b(i) ** 2)
    return res


def G(t, params):
    tau = params["t1"]
    b1 = params["b1"]
    b2 = params["b2"]
    b3 = params["b3"]
    return (
        b1
        + (b2 + b3) * (tau / t) * (1 - np.exp(-t / tau))
        - b3 * np.exp(-t / tau)
        + s(t, params)
    )


def Y(t, params):
    return 10_000 * (np.exp(G(t, params) / 10_000) - 1)


def yield_curve_parameters(date: str):
    e = Endpoint("/iss/history/engines/stock/zcyc")
    r = e.get(param=dict(date=date))
    return r["params"]


def yield_curve(date: str, t: float):
    params = yield_curve_parameters(date)[-1]
    return Y(t, params)

