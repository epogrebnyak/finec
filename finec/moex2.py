# This file will be deleted.
# - corp bond
# - default names for stocks

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

import pandas as pd
import requests
from apimoex import ISSClient
from pandas._libs.missing import NAType


def assert_date(s: str) -> str:
    # date must be in YYYY-MM-DD format, passes now without check
    return s


def assert_endpoint(endpoint):
    if not endpoint.startswith("/iss"):
        raise ValueError(f"{endpoint} must start with '/iss'.")


def qualified(endpoint):
    return "https://iss.moex.com" + endpoint + ".json"


def get(endpoint, param={}):
    assert_endpoint(endpoint)
    with requests.Session() as session:
        return ISSClient(session, qualified(endpoint), param).get()


def get_all(endpoint, param={}):
    assert_endpoint(endpoint)
    with requests.Session() as session:
        return ISSClient(session, qualified(endpoint), param).get_all()


@dataclass
class Query:
    endpoint: str
    param: dict = field(default_factory=dict)

    def __post_init__(self):
        assert_endpoint(self.endpoint)

    @property
    def url(self):
        return qualified(self.endpoint)

    def get(self):
        with requests.Session() as session:
            return ISSClient(session, self.url, self.param).get()

    def get_all(self):
        with requests.Session() as session:
            return ISSClient(session, self.url, self.param).get_all()


def find(query_str: str, is_traded=True):
    param = dict(q=query_str)
    param["is_trading"] = "1" if is_traded else "0"
    # Note: possibly still limits output to 100 items
    return get_all(endpoint="/iss/securities", param=param)["securities"]


def describe(ticker: str):
    return get(f"/iss/securities/{ticker}")["description"]


def board_dict(ticker: str):
    return get(f"/iss/securities/{ticker}")["boards"]


def traded_boards(ticker: str):
    return [d["boardid"] for d in board_dict(ticker) if d["is_traded"] == 1]


assert traded_boards("AFLT") == [
    "TQBR",
    "SPEQ",
    "SMAL",
    "TQDP",
    "RPMO",
    "PTEQ",
    "PSEQ",
    "RPEU",
    "RPEO",
    "EQRD",
    "EQRE",
    "EQWP",
    "EQWD",
    "EQWE",
    "EQRP",
    "LIQR",
    "EQRY",
    "PSRY",
    "PSRP",
    "PSRD",
    "PSRE",
    "LIQB",
]


class ValidColumns:
    security_bond = [  # security
        "SECID",
        "SECNAME",
        "SHORTNAME",
        "LATNAME",
        "BOARDID",
        "BOARDNAME",
        "LISTLEVEL",
        "STATUS",
        "ISIN",
        "REGNUMBER",
        "MARKETCODE",
        "INSTRID",
        "SECTORID",
        "SECTYPE",
        "CURRENCYID",
        "DECIMALS",
        "MINSTEP",
        "LOTSIZE",
        "LOTVALUE",
        "FACEUNIT",
        "FACEVALUE",
        "ISSUESIZE",
        "ISSUESIZEPLACED",
        "REMARKS",
        # latest quote
        "OFFERDATE",
        "MATDATE",
        "BUYBACKDATE",
        "BUYBACKPRICE",
        "COUPONPERCENT",
        "COUPONVALUE",
        "COUPONPERIOD",
        "NEXTCOUPON",
        "ACCRUEDINT",
        "SETTLEDATE",
        "PREVDATE",
        "PREVPRICE",
        "YIELDATPREVWAPRICE",
    ]

    security_currency = [
        "SECID",
        "BOARDID",
        "MARKETCODE",
        "SECNAME",
        "SHORTNAME",
        "SETTLEDATE",
        "PREVPRICE",
        "PREVWAPRICE",
        "PREVDATE",
        "CURRENCYID",
    ]

    history_bond = [
        "TRADEDATE",
        "BOARDID",
        "HIGH",
        "LOW",
        "OPEN",
        "CLOSE",
        "WAPRICE",
        "YIELDCLOSE",
        "NUMTRADES",
        "VALUE",
        "VOLUME",
        "MATDATE",
        "OFFERDATE",
        "BUYBACKDATE",
        "DURATION",
        "COUPONPERCENT",
        "COUPONVALUE",
        "ACCINT",
        "FACEVALUE",
        "FACEUNIT",
        "CURRENCYID",
    ]

    history_stock = [
        "TRADEDATE",
        "BOARDID",
        "HIGH",
        "LOW",
        "OPEN",
        "CLOSE",
        "WAPRICE",
        "NUMTRADES",
        "VALUE",
        "VOLUME",
    ]


def history_endpoint(engine, market, board, security):
    return (
        f"/iss/history/engines/{engine}"
        f"/markets/{market}"
        f"/boards/{board}/"
        f"securities/{security}"
    )


def board_quote(engine, market, board, security, param={}):
    endpoint = history_endpoint(engine, market, board, security)
    return get_all(endpoint, param)["history"]


def stock_history(
    security, board="TQBR", columns=ValidColumns.history_stock, start=None, end=None
):
    param = make_query_dict(columns, start, end)
    return board_quote("stock", "shares", board, security, param)


def bond_history(
    security, board="TQCB", columns=ValidColumns.history_bond, start=None, end=None
):
    param = make_query_dict(columns, start, end)
    return board_quote("stock", "bonds", board, security, param)


def names(dict_list: List[dict]):
    return [d["name"] for d in dict_list]


def history_endpoint(engine, market, board, security):
    return (
        f"/iss/history/engines/{engine}"
        f"/markets/{market}"
        f"/boards/{board}/"
        f"securities/{security}"
    )


# TQCB, TQOB
# state_bonds = Board(engine="stock", market="bonds", board="TQCB")
# corp_bonds = Board(engine="stock", market="bonds", board="TQ0B")
# this is corporate bonds - for government bonds need TQ0B
def get_bonds_board(board="TQOB"):
    # use /history/
    pass
