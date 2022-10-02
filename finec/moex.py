"""finec.moex - Data retrieval from MOEX statistics server.

Developped by Evgeny Pogrebnyak, Finec MGIMO.

Based on @WLMike1 apimoex.ISSClient and apimoex project. 

Installation:

  pip install git+https://github.com/epogrebnyak/finec.git

Retrieve daily quotes by instrument as pandas dataframes:

  from finec.moex import Stock, Bond, Currency, find

  Stock("YNDX").get_history()
  Bond(ticker="RU000A101NJ6", board="TQIR").get_history()
  Currency("USD000UTSTOM").get_history(start="2020-01-01")

Tell more about securities:

  Stock("YNDX").whoami()
  Bond(ticker="RU000A101NJ6", board="TQIR").provided_columns()
  find("Челябинский")
"""

from dataclasses import dataclass, field
from typing import ClassVar, Dict, List, Optional, Union

import pandas as pd
import requests
from apimoex import ISSClient
from pandas._libs.missing import NAType

from finec.dividend import get_dividend

__all__ = [
    "find",
    "whoami",
    "Stock",
    "Index",
    "Bond",
    "Currency",
    "CURRENCIES",
    "MARKETS",
    "BOARDS",
]


#%%

from dataclasses import dataclass


@dataclass
class Endpoint:
    locator: str

    def __post_init__(self):
        if not self.locator.startswith("/iss"):
            raise ValueError(f"{self.locator} must start with '/iss'.")

    @property
    def qualified(self):
        return "https://iss.moex.com" + self.locator + ".json"

    def get_with(self, func_name: str, param: Dict = {}):
        with requests.Session() as session:
            client = ISSClient(session, self.qualified, param)
            caller = getattr(client, func_name)
            return caller()

    def get(self, param: Dict = {}):
        return self.get_with("get", param)

    def get_all(self, param: Dict = {}):
        return self.get_with("get_all", param)


#%%


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


def find(query_str: str, is_traded=True):
    param = dict(q=query_str)
    param["is_trading"] = "1" if is_traded else "0"
    # Note: possibly limits output to 100 items regardless of get_all
    return get_all(endpoint="/iss/securities", param=param)["securities"]


def describe_json(ticker: str):
    return get(f"/iss/securities/{ticker}")["description"]


def whoami(ticker: str):
    return {d["name"]: d["value"] for d in describe_json(ticker)}


def all_boards(ticker: str):
    return get(f"/iss/securities/{ticker}")["boards"]


def traded_boards(ticker: str):
    return {d["boardid"]: d["title"] for d in all_boards(ticker) if d["is_traded"] == 1}


def endpoint(base, engine, market, board="", ticker=""):
    assert_endpoint(base)
    res = base + f"/engines/{engine}/markets/{market}"
    if board:
        res += f"/boards/{board}"
    if ticker:
        res += f"/securities/{ticker}"
    return res


def history_endpoint(engine, market, board="", ticker=""):
    return endpoint("/iss/history", engine, market, board, ticker)


def dataframe(json_dict) -> pd.DataFrame:
    df = pd.DataFrame(json_dict)
    if "TRADEDATE" in df.columns:
        df["TRADEDATE"] = pd.to_datetime(df["TRADEDATE"])
        df = df.set_index("TRADEDATE")
    date_cols = ["MATDATE", "OFFERDATE", "BUYBACKDATE"]
    for col in date_cols:
        if col in df.columns:
            df[col] = df[col].map(as_date)
    return df


def get_engines() -> Dict:
    return {d["name"]: d["title"] for d in get("/iss/engines/")["engines"]}


@dataclass
class Engine:
    engine: str

    def market(self, market):
        return Market(self.engine, market)

    @property
    def endpoint(self):
        return f"/iss/engines/{self.engine}"

    def describe(self):
        return get(self.endpoint)

    def markets(self) -> Dict:
        ds = get(self.endpoint + "/markets")["markets"]
        return {d["NAME"]: d["title"] for d in ds}


@dataclass
class Market(Engine):
    engine: str
    market: str

    @property
    def endpoint(self):
        return f"/iss/engines/{self.engine}/markets/{self.market}"

    def boards(self) -> List:
        return [d["boardid"] for d in self.describe()["boards"]]

    def traded_boards(self) -> List:
        return [d["boardid"] for d in self.describe()["boards"] if d["is_traded"]]

    def volumes(self) -> pd.DataFrame:
        return (
            self.history()[["BOARDID", "VALUE"]]
            .groupby("BOARDID")
            .sum()
            .divide(1e6)
            .round(1)
            .query("VALUE != 0")
            .VALUE.sort_values(ascending=False)
        )

    def board(self, board: str):
        return Board(self.engine, self.market, board)

    def securities(self) -> pd.DataFrame:
        # /securities endpoint returns dict with following keys:
        # ['securities', 'marketdata', 'dataversion', 'marketdata_yields']
        # - 'securities' is returned by this method
        # - 'marketdata' is not meaningful data
        # - 'dataversion' is a timestamp
        # - 'marketdata_yields' is non-empty for bonds- returned by yields
        return dataframe(get(self.endpoint + "/securities")["securities"])

    def tickers(self) -> List[str]:
        return self.securities()["SECID"].unique().tolist()

    def yields(self) -> pd.DataFrame:
        return dataframe(get(self.endpoint + "/securities")["marketdata_yields"])

    @property
    def history_endpoint(self):
        return f"/iss/history/engines/{self.engine}/markets/{self.market}"

    def history_json(self) -> List:
        return get_all(self.history_endpoint + "/securities")["history"]

    def history(self) -> pd.DataFrame:
        return dataframe(self.history_json())

    def volume(self) -> Optional[int]:
        try:
            return self.history()["VOLUME"].sum()
        except KeyError:
            return None


class Markets:
    stocks = Market("stock", "shares")
    bonds = Market("stock", "bonds")
    currency = Market("currency", "selt")


MARKETS = [Markets.stocks, Markets.bonds, Markets.currency]


@dataclass
class Board(Market):
    engine: str
    market: str
    board: str

    @property
    def endpoint(self):
        return f"/iss/engines/{self.engine}/markets/{self.market}/boards/{self.board}"

    @property
    def history_endpoint(self):
        return f"/iss/history/engines/{self.engine}/markets/{self.market}/boards/{self.board}"


def stocks_board(board: str = "TQBR") -> Board:
    return Markets.stocks.board(board)


def bonds_board(board: str) -> Board:
    return Markets.bonds.board(board)


def corporate_bonds_board() -> Board:
    return bonds_board("TQCB")


def federal_bonds_board() -> Board:
    return bonds_board("TQOB")


def currencies_board(board: str = "CETS") -> Board:
    return Markets.currency.board(board)


BOARDS = [
    stocks_board(),
    corporate_bonds_board(),
    federal_bonds_board(),
    currencies_board(),
]


def stock_prices(b: Board):
    # fmt: off
    columns = [
        "BOARDID", "SECID", "SHORTNAME", 
        "OPEN", "LOW", "HIGH", "CLOSE", "WAPRICE",
        "NUMTRADES", "VALUE", "VOLUME"
    ]
    # fmt: on
    return (
        b.history()
        .query("NUMTRADES > 0")[columns]
        .sort_values("VALUE", ascending=False)
    )


def stocks_dataframe():
    b = stocks_board()
    return stock_prices(b)


def bond_prices(b: Board) -> pd.DataFrame:
    # fmt: off
    columns = [
           'BOARDID', 'SHORTNAME', 'SECID',
           'NUMTRADES', 'VALUE', 'VOLUME', 'CLOSE',
           'ACCINT', 'COUPONPERCENT', 'COUPONVALUE',
           'YIELDCLOSE', 'YIELDTOOFFER', 'YIELDLASTCOUPON',
           'MATDATE', 'OFFERDATE', 'DURATION',
           'BUYBACKDATE', 'LASTTRADEDATE',
           'FACEVALUE', 'CURRENCYID', 'FACEUNIT']
    # fmt: on
    return b.history().query("NUMTRADES>0")[columns]


def bond_yields(b: Board) -> pd.DataFrame:
    df = b.yields().drop(columns="IR ICPI BEI CBR SEQNUM".split())
    # Convert to date columns
    for col in ["YIELDDATE", "ZCYCMOMENT"]:
        df[col] = pd.to_datetime(df[col])
    # Considering ZCYCMOMENT a proxy for trading date, may review
    df["TERM"] = (df["YIELDDATE"] - df["ZCYCMOMENT"]).map(lambda x: x.days / 365)
    return df


def bonds_dataframe():
    b = corporate_bonds_board()
    df = bond_prices(b)
    return df.merge(bond_yields(b), how="left", on="SECID")


def securities(endpoint: str):
    return get(endpoint + "/securities")


def make_query_dict(columns, start, end):
    param = {}
    if columns:
        param["history.columns"] = ",".join(columns)
    if start:
        param["from"] = assert_date(start)
    if end:
        param["till"] = assert_date(end)
    return param


def quote(b: Board, ticker: str, columns=[], start="", end=""):
    endpoint = history_endpoint(b.engine, b.market, b.board, ticker)
    param = make_query_dict(columns, start, end)
    return get_all(endpoint, param)["history"]


def default(value):
    return field(repr=False, default=value)


ClassList = ClassVar[Optional[List[str]]]


@dataclass
class Security:
    ticker: str
    board: str = ""
    engine: str = default("")
    market: str = default("")
    default_columns: ClassList = None

    def whoami(self):
        return whoami(self.ticker)

    @property
    def board_obj(self):
        return Board(self.engine, self.market, self.board)

    @property
    def history_endpoint(self):
        return history_endpoint(self.engine, self.market, self.board, self.ticker)

    def provided_columns(self):
        sample_dicts = get(self.history_endpoint)["history"]
        return list(sample_dicts[0].keys())

    def get_history_json(self, columns=[], start="", end=""):
        """ "Use columns=None to get all columns, showing default_columns otherwise."""
        if columns == []:
            columns = self.default_columns
        return quote(self.board_obj, self.ticker, columns, start, end)

    def get_history(self, columns=[], start="", end=""):
        return dataframe(self.get_history_json(columns, start, end))

    def get_candles(self, interval=24, columns=[], start="", end=""):
        # "https://iss.moex.com/iss/engines/{engine}/markets/{market}/"
        # f"boards/{board}/securities/{security}/candles.json"
        pass


@dataclass
class Stock(Security):
    ticker: str
    board: str = "TQBR"
    engine: str = default("stock")
    market: str = default("shares")
    default_columns: ClassList = [
        "TRADEDATE",
        "SECID",
        "BOARDID",
        "CLOSE",
        "WAPRICE",
        "NUMTRADES",
        "VALUE",
        "VOLUME",
    ]

    def get_dividend(self):
        return get_dividend(self.ticker)


industries = dict(
    oilgas="GAZP LKOH SNGS SNGSP TATN TATNP NVTK TRNFP ROSN",
    retail="FIVE FIXP DSKY MGNT",
    mm="ALRS GMKN NLMK RUAL POLY CHMF PLZL MAGN POGR PHOR",
    finance="MOEX TCSG SBER SBERP VTBR CBOM",
    construction="PIKK",
    diversified="AFKS",
    transport="AFLT GLTR",
    technology="HHRU OZON YNDX VKCO",
    telecom="MTSS RTKM",
    power="HYDR IRAO FEES ENPG",
)


def industry(ticker: str) -> str:
    d = {v: k for k, vs in industries.items() for v in vs.split()}
    return d.get(ticker, "not specified")


@dataclass
class Bond(Security):
    ticker: str
    board: str = "TQCB"
    engine: str = default("stock")
    market: str = default("bonds")
    default_columns: ClassList = [
        "TRADEDATE",
        "BOARDID",
        "SECID",
        "CLOSE",
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


@dataclass
class Index(Security):
    ticker: str
    board: str = "SNDX"
    engine: str = default("stock")
    market: str = default("index")
    default_columns: ClassList = None

    def composition(self):
        """
        Implemented as in https://github.com/WLM1ke/apimoex/issues/12
        See https://www.moex.com/ru/index/IMOEX/constituents/
        """
        endpoint = (
            f"/iss/statistics/engines/stock/markets/index/analytics/{self.ticker}"
        )
        return get_all(endpoint)["analytics"]

    def tickers(self):
        return [d["ticker"] for d in self.composition()]


@dataclass
class Currency(Security):
    # https://iss.moex.com/iss/engines/currency/markets/selt/boards/CETS/securities
    # https://www.moex.com/s135
    ticker: str
    board: str = "CETS"
    engine: str = default("currency")
    market: str = default("selt")
    default_columns: ClassList = None


CURRENCIES = dict(
    USDRUR=Currency("USD000UTSTOM"),
    EURRUR=Currency("EUR_RUB__TOM"),
    CNYRUR=Currency("CNYRUB_TOM"),
)


def get_bonds_market():
    """
    Equivalent to Market(engine='stock', market='bonds').securities()
    """
    return get("/iss/engines/stock/markets/bonds/securities")["securities"]


def get_bond_market_yields():
    """
    Equivalent to Market(engine='stock', market='bonds').yields()
    """
    return get("/iss/engines/stock/markets/bonds/securities")["marketdata_yields"]


def get_stocks_market():
    """
    Equivalent to Market(engine='stock', market='shares').securities()
    """
    return get("/iss/engines/stock/markets/shares/securities")["securities"]


def get_currencies_market():  # not tested
    """
    Equivalent to Market(engine='currency', market='selt').securities()
    """
    return get("/iss/engines/currency/markets/selt/securities")["securities"]


def get_indices_market():
    """
    Equivalent to Market(engine='currency', market='index').securities()
    """
    return get("/iss/engines/stock/markets/index/securities")["securities"]


def as_date(s: str) -> Union[pd.Timestamp, NAType]:
    try:
        return pd.Timestamp(s)
    except ValueError:
        return pd.NA


def yield_jsons_by_field(security_class, tickers, field):
    import tqdm

    columns = ["TRADEDATE", "SECID", field]
    for t in tqdm.tqdm(tickers):
        for j in security_class(t).get_history_json(columns):
            if j[field]:
                yield j


def save_tickers(path, security_class, tickers, field):
    gen = yield_jsons_by_field(security_class, tickers, field="CLOSE")
    df = pd.DataFrame(gen).pivot(index="TRADEDATE", columns="SECID", values=field)
    df.to_csv(path)
