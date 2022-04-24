"""finec.moex - Data retrieval from MOEX statistics server.

Developped by Evgeny Pogrebnyak, Finec MGIMO.

Based on @WLMike1 apimoex.ISSClient and apimoex project. 

Installation:

  pip install git+https://github.com/epogrebnyak/finec.git

Retrieve daily quotes by instrument as pandas dataframes:

  from finec.moex import Stock, Bond, Currency, dataframe, find

  Stock("YNDX").get_history()
  Bond(ticker="RU000A101NJ6", board="TQIR").get_history()
  Currency("USD000UTSTOM").get_history(start="2020-01-01")

Tell more about securities:

  Stock("YNDX").whoami()
  Bond(ticker="RU000A101NJ6", board="TQIR").provided_columns()
  find("Челябинский")


User questions:

- What classes of securities are available?
  Stock, Bond, Index, Currency

- What is the ticker list for this class of security (eg all tickers for stocks)?
  status: not implemented, superceded by next question

- What are the latest quotes for all securities of the class (eg all corporate bonds)?
  status: experimental
  unclear of the source - market/secirities or board/securities?
                          and /iss and /iss/history base

- What is the quote history for a security (eg YNDX, AFLT, SBER, MTSS or RU000A101NJ6)?
  status: implemented, tested

Supplementary questions:

- At what board a security is traded?

  import finec.moex as moex
  moex.traded_boards("MTSS")

- What are the boards for each security class?

  # not tested
  moex.Market("stock", "shares").boards()

Unanswered:

- How can I get a nice dataset of the bonds market yields and durations?
- Can MOEX bond yield calculation be trusted?
- Why do column lists differ across endpoints?
- Can issuer ticker be linked to company tax number?
- Are government bonds included in TQCB board?
- Why are there so many boards?
"""

from dataclasses import dataclass, field
from typing import ClassVar, Dict, List, Optional, Union

import pandas as pd
import requests
from apimoex import ISSClient
from pandas._libs.missing import NAType

__all__ = [
    "find",
    "describe",
    "traded_boards",
    "Stock",
    "Index",
    "Bond",
    "Currency",
    "get_stocks",
    "get_bonds",
    "get_bond_yields",
    "get_currencies",
    "usd_rur",
    "eur_rur",
    "cny_rur",
    "dataframe",
]


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
    return {d["boardid"]: d["title"] for d in board_dict(ticker) if d["is_traded"] == 1}


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


@dataclass
class Market:
    engine: str
    market: str

    @property
    def endpoint(self):
        return f"/iss/engines/{self.engine}/markets/{self.market}"

    @property
    def history_endpoint(self):
        return f"/iss/history/engines/{self.engine}/markets/{self.market}"

    def describe(self):
        return get(self.endpoint)

    def securities(self) -> Dict:
        return get(self.endpoint + "/securities")

    def securities_history(self) -> Dict:
        return get(self.history_endpoint + "/securities")

    def _boards(self) -> List:
        return get(self.endpoint + "/boards")["boards"]

    def boards(self):
        return {d["boardid"]: d["title"] for d in self._boards()}

    def traded_boards(self):
        return {d["boardid"]: d["title"] for d in self._boards() if d["is_traded"] == 1}


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


def securities(endpoint: str):  # not tested
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
        return {d["name"]: d["value"] for d in describe(self.ticker)}

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


@dataclass
class Stock(Security):
    ticker: str
    board: str = "TQBR"
    engine: str = default("stock")
    market: str = default("shares")
    default_columns: ClassList = [
        "TRADEDATE",
        "BOARDID",
        "CLOSE",
        "WAPRICE",
        "NUMTRADES",
        "VALUE",
        "VOLUME",
    ]


@dataclass
class Bond(Security):
    ticker: str
    board: str = "TQCB"
    engine: str = default("stock")
    market: str = default("bonds")
    default_columns: ClassList = [
        "TRADEDATE",
        "BOARDID",
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
        # Implemented as in https://github.com/WLM1ke/apimoex/issues/12
        # On web see https://www.moex.com/ru/index/IMOEX/constituents/
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


def usd_rur():
    return Currency("USD000UTSTOM")


def eur_rur():
    return Currency("EUR_RUB__TOM")


def cny_rur():
    return Currency("CNYRUB_TOM")


def get_bonds():
    return get("/iss/engines/stock/markets/bonds/securities")["securities"]


def get_bond_yields():
    return get("/iss/engines/stock/markets/bonds/securities")["marketdata_yields"]


def get_stocks():
    return get("/iss/engines/stock/markets/shares/securities")["securities"]


def get_currencies():  # not tested
    return get("/iss/engines/currency/markets/selt/securities")["securities"]


def get_indices():
    return get("/iss/engines/stock/markets/index/securities")["securities"]


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


def yield_fields(cls, tickers, field="CLOSE"):
    import tqdm

    columns = ["TRADEDATE", "SECID"] + [field]
    for t in tqdm.tqdm(tickers):
        for j in cls(t).get_history_json(columns):
            if j[field]:
                yield j


def save_generator(filename, gen, field):
    df = pd.DataFrame(gen).pivot(index="TRADEDATE", columns="SECID", values=field)
    df.to_csv(filename)
