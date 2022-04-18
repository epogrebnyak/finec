from typing import Dict, Union

import pandas as pd
import requests
from apimoex import ISSClient
from pandas._libs.missing import NAType
from typing import List, Optional

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
    param["is_trading"] = "1" if is_traded else "0"
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


def assert_date(s: str) -> str:
    # date must be in YYYY-MM-DD format, pass now without check
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


def index_history(
    security, board="SNDX", columns=None, start=None, end=None
):  # not tested
    # index_history("IMOEX")
    param = make_query_dict(columns, start, end)
    return board_quote("stock", "index", board, security, param)


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


# maybe use a dataclass
from dataclasses import dataclass


@dataclass
class Market:
    engine: str
    market: str

    @property
    def endpoint(self):
        return f"/iss/engines/{self.engine}/markets/{self.market}"

    def describe(self):
        return get(self.endpoint)

    def securities(self) -> Dict:
        return get(self.endpoint + "/securities")

    def columns(self) -> Dict:
        # must select key in output dict
        return get(self.endpoint + "/securities/columns")

    def boards(self) -> List:
        return get(self.endpoint + "/boards")["boards"]


class MarketHistory(Market):
    engine: str
    market: str

    @property
    def endpoint(self):
        return f"/iss/history/engines/{self.engine}/markets/{self.market}"

    def columns(self) -> Dict:
        return get(self.endpoint + "/securities/columns")["history"]

    def securities(self):
        return get(self.endpoint + "/securities")


@dataclass
class Board:
    engine: str
    market: str
    board: str

    @property
    def endpoint(self):
        return f"/iss/engines/{self.engine}/markets/{self.market}/boards/{self.board}"

    def describe(self):
        return get(self.endpoint)

    def securities(self):
        return get(self.endpoint + "/securities")


@dataclass
class BoardHistory:
    engine: str
    market: str
    board: str

    @property
    def endpoint(self):
        return f"/iss/history/engines/{self.engine}/markets/{self.market}/boards/{self.board}"

    def securities(self):
        return get_all(self.endpoint + "/securities")["history"]


def describe(ticker):
    return get(f"/iss/securities/{ticker}")["description"]


def boards(ticker):
    return get(f"/iss/securities/{ticker}")["boards"]


@dataclass
class Quoter:
    board: Board
    columns: Optional[List[str]] = None

    def get_history(self, ticker: str, start=None, end=None):
        param = make_query_dict(self.columns, start, end)
        return self.board.history.quote(self.ticker, param)


stocks = Quoter(
    Board("stock", "shares", "TQBR"),
    columns=[
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
    ],
)


def history_endpoint(engine, market, board, security):
    return (
        f"/iss/history/engines/{engine}"
        f"/markets/{market}"
        f"/boards/{board}/"
        f"securities/{security}"
    )


stocks = Board("stocks", "shares", "TQBR")
corp_bonds = Board("stocks", "bonds", "TQBR")

# TQCB, TQOB
# state_bonds = Board(engine="stock", market="bonds", board="TQCB")
# corp_bonds = Board(engine="stock", market="bonds", board="TQ0B")
# this is corporate bonds - for government bonds need TQ0B
def get_bonds_board(board="TQOB"):
    # use /history/
    pass


def get_bonds():
    return get("/iss/engines/stock/markets/bonds/securities")["securities"]


def get_bond_yields():
    return get("/iss/engines/stock/markets/bonds/securities")["marketdata_yields"]


def get_shares():
    return get("/iss/engines/stock/markets/shares/securities")["securities"]


def get_currencies():  # not tested
    return get("/iss/engines/currency/markets/selt/securities")["securities"]


def get_indices():
    return get("/iss/engines/stock/markets/index/securities")["securities"]
