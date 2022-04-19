from dataclasses import dataclass, field
from typing import List, ClassVar
from moex import history_endpoint, get_all, get, qualified, MarketHistory, make_query_dict, assert_endpoint

def endpoint(base, engine, market, board="", ticker=""):
    assert_endpoint(base)
    res = base + f"/engines/{engine}/markets/{market}"
    if board:
       res+= f"/boards/{board}/"
    if ticker:
       res += f"securities/{ticker}"    
    return res   

def base_endpoint(engine, market, board="", ticker=""):
    return endpoint("/iss", engine, market, board, ticker)

def history_endpoint(engine, market, board="", ticker=""):
    return endpoint("/iss/history", engine, market, board, ticker)

@dataclass
class Board:
    engine: str
    market: str
    board: str

    @property 
    def history_endpoint(self, ticker):
        return history_endpoint(self.engine, self.market, self.board, ticker)

    @property
    def base_endpoint(self):
        return base_endpoint(self.engine, self.market, self.board)

    def describe(self):
        return get(self.endpoint)    

    def _securities(self): #experimental
        return get(self.endpoint + "/securities")


def quote(b: Board, ticker: str, columns=[], start="", end=""):
    endpoint = history_endpoint(b.engine, b.market, b.board, ticker)
    param = make_query_dict(columns, start, end)
    return get_all(endpoint, param)["history"]

@dataclass
class Security:
    ticker: str
    board: str


def default(value):
    return field(repr=False, default=value)

ClassList = ClassVar[List[str]]

@dataclass
class Stock(Security):
    ticker: str
    board: str = "TQBR"
    engine: str = default("stock")
    market: str = default("shares")
    columns: ClassList = [
        "TRADEDATE",
        "BOARDID",
        "HIGH",
        "LOW",
        "OPEN",
        "CLOSE",
        "VALUE",
        "VOLUME",
    ]

    @property
    def _board(self):
        return Board(self.engine, self.market, self.board)

    @property
    def history_endpoint(self):
        return self._board.history_endpoint(self.ticker)

    def describe_columns(self):
        return MarketHistory(self.engine, self.market).columns()["securities"]

    def available_columns(self):
        return [d["name"] for d in self.describe_columns()]

    def get_history(self, columns=[], start="", end=""):
        if columns == []:
            columns = self.columns
        return quote(self._board, self.ticker, columns, start, end)

# TODO: move to tests
s = Stock("YNDX")
res = s.get_history(start="2022-04-15", end="2022-04-15")
assert res == [{'TRADEDATE': '2022-04-15', 'BOARDID': 'TQBR', 'HIGH': 1996, 'LOW': 1900.2, 'OPEN': 1955.4, 'CLOSE': 1979.6, 'VALUE': 670094691.8, 'VOLUME': 343213}]
assert list(res[0].keys()) == s.columns
assert qualified(s.history_endpoint) == "https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/YNDX.json"
assert s.available_columns() == ['SECID', 'BOARDID', 'SHORTNAME', 'PREVPRICE', 'LOTSIZE', 'FACEVALUE', 'STATUS', 'BOARDNAME', 'DECIMALS', 'SECNAME', 'REMARKS', 'MARKETCODE', 'INSTRID', 'SECTORID', 'MINSTEP', 'PREVWAPRICE', 'FACEUNIT', 'PREVDATE', 'ISSUESIZE', 'ISIN', 'LATNAME', 'REGNUMBER', 'PREVLEGALCLOSEPRICE', 'PREVADMITTEDQUOTE', 'CURRENCYID', 'SECTYPE', 'LISTLEVEL', 'SETTLEDATE']
assert len(s.describe_columns()) > 0 

# User questions:
# - What classes of securities are available (stock, bond, index, currency)? 
# - What is ticker list for this class of security (eg all tickers for stocks)? 
# - What are the last trading day quotes for all securities of the class (eg all corporate bonds)?
# - What is the quote history for a security (eg YNDX, AFLT, SBER, MTSS)?

# Also must know: 
# - At what board a security is traded? 
# - What are the boards for each security class? 
