[![Tests](https://github.com/epogrebnyak/finec/actions/workflows/.pytest.yml/badge.svg)](https://github.com/epogrebnyak/finec/actions/workflows/.pytest.yml)
[![Finec version](https://badgen.net/pypi/v/finec)](https://pypi.org/project/finec/)

# finec

Financial data and financial computation utilities for Finec MGIMO students.

## Demo application

<https://share.streamlit.io/epogrebnyak/finec/main>

## Installation

```console
pip install git+https://github.com/epogrebnyak/finec.git
```

## Moscow Exchange (MOEX)

Download Moscow Exchange (MOEX) data for stocks, bonds, currencies and indices as pandas dataframes, CSV or Excel files.

### Stocks

```python
from finec.moex import Stock, Index

# What stocks are part of IMOEX index?
Index("IMOEX").composition()

# General information about Aeroflot stock
Stock("AFLT").whoami()

# Ozon stock price history, all dates and columns
Stock("OZON").get_history()

# Yandex stock price, restricted by columns and start date
Stock("YNDX").get_history(columns=["TRADEDATE", "CLOSE"], start="2022-01-01")

# Get dividend history from https://github.com/WLM1ke/poptimizer
Stock("GMKN").get_dividend()
```

### Bonds

```python
from finec.moex import Bond

# Sistema 2027 bond price and yields from TQCB trading bord
Bond(ticker="RU000A0JXN21", board="TQCB").get_history()

# What data columns are provided for trading history?
Bond(ticker="RU000A101NJ6", board="TQIR").provided_columns()
```

### Currencies

```python
from finec.moex import Currency, CURRENCIES

# Tickers for usd, euro and yuan exchange rates
USDRUR = Currency(ticker='USD000UTSTOM', board='CETS')
EURRUR = Currency(ticker='EUR_RUB__TOM', board='CETS')
CNYRUR = Currency(ticker='CNYRUB_TOM', board='CETS')

# USDRUR exchange rate starting 2020
USDRUR.get_history(start="2020-01-01")
```

### Lookup functions

```python
from finec.moex import whoami, find, traded_boards

# General information about ticker
whoami("YNDX")

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

# trading volumes by board
b.volumes()

# securitites list
b.securities()

# last trading day quotes
b.history()
```

### More about MOEX data

References:

- MOEX API reference <https://iss.moex.com/iss/reference/?lang=en>
- Developper manual (2016) <https://fs.moex.com/files/6523>

Notes:

- MOEX is very generious to provide a lot of data for free and without any registration or tokens.
- MOEX API provided on "as is" basis and some parts are undocumented.

## Aknowledgements

- We rely on `apimoex.ISSClient` and expertise developped within [apimoex project](https://github.com/WLM1ke/apimoex) by [@WLMike1](https://github.com/WLM1ke).
- Dividend history relayed from <https://github.com/WLM1ke/poptimizer>
