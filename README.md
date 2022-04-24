[![Tests](https://github.com/epogrebnyak/finec/actions/workflows/.pytest.yml/badge.svg)](https://github.com/epogrebnyak/finec/actions/workflows/.pytest.yml)

# finec

Financial data and financial computation utilities for Finec MGIMO students.

## Installation

```console
pip install git+https://github.com/epogrebnyak/finec.git
```

## Moscow Exchange (MOEX)

Get Moscow Exchange (MOEX) data for stocks, bonds, currencies and indices as pandas dataframe. 

`(*)` denotes lower level functions, skip at first reading.

### Stocks

```python
from finec.moex import Stock, Index
from finec.dividend import get_dividend

# What stocks are in IMOEX index? 
Index("IMOEX").composition()

# Aeroflot stock information
Stock("AFLT").whoami()

# Ozon stock price history
Stock("OZON").get_history(columns=["TRADEDATE", "CLOSE"])

# Yandex stock price
Stock("YNDX").get_history(start="2022-01-01")

# Get dividend history from https://github.com/WLM1ke/poptimizer
get_dividend(ticker="GMKN")
```

### Bonds

```python 
from finec.moex import Bond

# Sistema 2027 bond price and yields from TQCB trading bord
Bond(ticker="RU000A0JXN21", board="TQCB").get_history()

# (*) What data columns are provided provide for trading history?
Bond(ticker="RU000A101NJ6", board="TQIR").provided_columns()
```

### Currencies

```python
from finec.moex import Currency, usd_rur, eur_rur, cny_rur 

# USDRUR exchange rate
Currency("USD000UTSTOM").get_history(start="2020-01-01")

# Tickers for euro and yuan exchange rates
eur_rur().ticker
cny_rur().ticker
```

### Lookup functions

```python 
from finec.moex import describe, find, traded_boards

# General information about ticker
describe("YNDX")  

# What boards does a security trade at?
traded_boards("MTSS")

# Are there traded securities with *query_str* in description?
find(query_str="Челябинский", is_traded=True)
```

### Markets and boards

```python 
from finec.moex import Market, Board

m = Market(engine="stock", market="shares")
m.traded_boards()

b = Board(engine="stock", market="shares", board="TQBR")
```

### More about MOEX data

References:

- MOEX API reference <https://iss.moex.com/iss/reference/?lang=en>
- Developper manual (2016) <https://fs.moex.com/files/6523>

Notes: 

- MOEX API is very generious to provide a lot of data for free and without any registration or tokens. 
- API provided on "as is" basis, some parts are undocumented.


## Aknowledgements

- We rely on `apimoex.ISSClient` and expertise developped within [apimoex project](https://github.com/WLM1ke/apimoex) by [@WLMike1](https://github.com/WLM1ke).
- Dividend history relayed from <https://github.com/WLM1ke/poptimizer>
