# pip install git+https://github.com/epogrebnyak/finec.git

from finec.moex import (
    Index,
    Market,
    dataframe,
    traded_boards,
    whoami,
    get,
    Stock,
    DEFAULT_BOARDS,
)

ds = Index("IMOEX").composition()
tickers = [d["ticker"] for d in ds]
