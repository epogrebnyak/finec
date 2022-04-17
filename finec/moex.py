from typing import Dict, Union

import pandas as pd
import requests
from apimoex import ISSClient

from pandas._libs.missing import NAType


__all__ = [
    "find",
    "stock_history",
    "bond_history",
    "currency_history",
    "get_bonds",
    "get_shares",
    "get_currencies",
    "usd_rur",
    "eur_rur",
    "cny_rur",
    "dataframe",
]


def start():
    return 1


def qualified(endpoint):
    if not endpoint.startswith("/iss"):
        raise ValueError(f"{endpoint} must start with '/iss'.")
    return "https://iss.moex.com" + endpoint + ".json"


def get(endpoint, param={}):
    with requests.Session() as session:
        return ISSClient(session, qualified(endpoint), param).get()


def get_all(endpoint, param={}):
    with requests.Session() as session:
        return ISSClient(session, qualified(endpoint), param).get_all()


def find(query_str: str, is_traded=True):
    # limits output to 100
    param = dict(q=query_str)
    param["is_trading"] = ("1" if is_traded else "0")
    return get_all(endpoint="/iss/securities", param=param)["securities"]


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
        "BOARDID" "HIGH",
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


def assert_date(s: str) -> str:
    # date must be in YYYY-MM-DD format
    return s


def make_query_dict(columns, start, end):
    param = {}
    if columns:
        param["history.columns"] = ",".join(columns)
    if start:
        param["from"] = assert_date(start)
    if end:
        param["till"] = assert_date(end)
    return param


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


def currency_history(security, board="CETS", columns=None, start=None, end=None):
    # https://iss.moex.com/iss/engines/currency/markets/selt/boards/CETS/securities
    # https://www.moex.com/s135
    param = make_query_dict(columns, start, end)
    return board_quote("currency", "selt", board, security, param)


def usd_rur(columns=None, start=None, end=None):
    return currency_history(
        security="USD000UTSTOM", columns=columns, start=start, end=end
    )


def eur_rur(columns=None, start=None, end=None):
    return currency_history(
        security="EUR_RUB__TOM", columns=columns, start=start, end=end
    )


def cny_rur(columns=None, start=None, end=None):
    return currency_history(
        security="CNYRUB_TOM", columns=columns, start=start, end=end
    )


def as_date(s: str) -> Union[pd.Timestamp, NAType]:
    try:
        return pd.Timestamp(s)
    except ValueError:
        return pd.NA


def dataframe(json_dict: Dict) -> pd.DataFrame:
    df = pd.DataFrame(json_dict)
    if "TRADEDATE" in df.columns:
        df["TRADEDATE"] = pd.to_datetime(df["TRADEDATE"])
        df = df.set_index("TRADEDATE")
    date_cols = ["MATDATE", "OFFERDATE", "BUYBACKDATE"]
    for col in date_cols:
        if col in df.columns:
            df[col] = df[col].map(as_date)
    return df


def get_bonds():
    return get("/iss/engines/stock/markets/bonds/securities")["securities"]


def get_shares():
    return get("/iss/engines/stock/markets/shares/securities")["securities"]


def get_currencies():  # not tested
    return get("/iss/engines/currency/markets/selt/securities")["securities"]

