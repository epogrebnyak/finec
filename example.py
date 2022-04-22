# pip install git+https://github.com/epogrebnyak/finec.git

from finec.moex import (
    Bond,
    Currency,
    Index,
    Market,
    Stock,
    dataframe,
    describe,
    find,
    traded_boards,
)

# Get history as JSONS
Stock("YNDX").get_history_json(start="2022-01-01")

# Get history as dataframes
Stock("YNDX").get_history()
Bond(ticker="RU000A101NJ6", board="TQIR").get_history()
Currency("USD000UTSTOM").get_history(start="2020-01-01")
Index("IMOEX").get_history(start="2021-12-01", end="2021-12-31")

# Security info
Stock("YNDX").whoami()  # identical to describe("YNDX")
Bond(ticker="RU000A101NJ6", board="TQIR").provided_columns()

# Lookup functions
describe("YNDX")
traded_boards("MTSS")
find("Челябинский")

# Market and board info
Market("stock", "shares").traded_boards()

# Index composition - as in https://www.moex.com/ru/index/IMOEX/constituents/
Index("IMOEX").composition()
