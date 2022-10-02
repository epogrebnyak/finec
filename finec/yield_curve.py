"""Получение параметров кривой бескупонной доходности и расчет доходности.

https://github.com/cmf-team/pricer/issues/3#issuecomment-1264697353

"""
#%%
from dataclasses import dataclass
import numpy as np
from finec.moex import Endpoint
from typing import Dict, Optional

#%%
a1 = 0
a2 = 0.6
k = 1.6


def fa(n: int):
    if n == 1:
        return a1
    if n == 2:
        return a2
    return fa(n - 1) + fa(2) * k ** (n - 2)


def fb(n: int):
    if n == 1:
        return fa(2)
    else:
        return fb(n - 1) * k


def s(t, params):
    res = 0
    for i in range(1, 9 + 1):
        g = params[f"g{i}"]
        res += g * np.exp(-((t - fa(i)) ** 2) / fb(i) ** 2)
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


@dataclass
class YieldCurve:
    iso_date: str
    params: Optional[Dict] = None

    def __post_init__(self):
        self.params = yield_curve_parameters(self.iso_date)

    @property
    def last(self):
        return self.params[-1]

    def rate(self, t: float):
        return Y(t, self.last)


#%%
import pandas as pd
from datetime import datetime


def make_date(iso_date: str):
    return datetime.strptime(iso_date, "%Y-%m-%d").strftime("%d.%m.%Y")


def make_url(iso_date: str):
    return "https://www.cbr.ru/hd_base/zcyc_params/zcyc/?DateTo={}".format(
        make_date(iso_date)
    )


def get_yields_from_cbr(iso_date: str) -> Dict[str, float]:
    df = pd.read_html(make_url(iso_date))[0]
    return df.iloc[:, 1:].T.to_dict()[0]


# %%
