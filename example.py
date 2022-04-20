# pip install git+https://github.com/epogrebnyak/finec.git

from finec.moex import (Bond, Currency, Market, Stock, dataframe, find,
                        traded_boards)

# Get history
dataframe(Stock("YNDX").get_history(start="2022-01-01"))
dataframe(Bond(ticker="RU000A101NJ6", board="TQIR").get_history())
dataframe(Currency("USD000UTSTOM").get_history(start="2022-01-01"))

# Security info
Stock("YNDX").whoami() # identical to describe("YNDX")
Bond(ticker="RU000A101NJ6", board="TQIR").provided_columns()

# Lookup functions
traded_boards("MTSS")
find("Челябинский")

# Market and board info
Market("stock", "shares").traded_boards()

#Index composition
Index("IMOEX").composition()
