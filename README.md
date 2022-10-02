<!--

Server unavailable outside Russia

-->

[![Tests](https://github.com/epogrebnyak/finec/actions/workflows/.pytest.yml/badge.svg)](https://github.com/epogrebnyak/finec/actions/workflows/.pytest.yml)
[![Finec version](https://badgen.net/pypi/v/finec)](https://pypi.org/project/finec/)

# finec

Financial data and financial computation utilities.

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

### Engines, markets and boards

```python
from finec.moex import get_engines, Engine, Market, Board

engines = get_engines()
print(engines)

e = Engine("forts")
e.markets()

m = Market(engine="stock", market="shares")
m.traded_boards()

b = Board(engine="stock", market="shares", board="TQBR")

# trading volumes by board
b.volumes()

# list securitites by board
b.securities()

# last trading day quotes by board
b.history()
```

### Yield curves

```python
from finec.yield_curve import YieldCurve, get_yields_from_cbr

y = YieldCurve("2022-09-28")
r1 = y.rate(t=1)
# 830.2383903307176

rs = get_yields_from_cbr("2022-09-28")
# {'0.25': 8.2, '0.50': 8.19, '0.75': 8.23, '1.00': 8.3, '2.00': 8.74, '3.00': 9.22, '5.00': 9.91, 
#  '7.00': 10.27, '10.00': 10.5, '15.00': 10.69, '20.00': 10.8, '30.00': 10.9}
```

### More about MOEX data

References:

- MOEX API reference <https://iss.moex.com/iss/reference/?lang=en>
- Developper manual (2016) <https://fs.moex.com/files/6523>

Notes:

- MOEX is very generious to provide a lot of data for free and without any registration or tokens.
- MOEX API provided on "as is" basis and some parts are undocumented.
- June 2022: MOEX statistics server not available for queries from Google Colab or Github Actions:
  - must use local installation for development
  - all remote tests on CI fail
  - streamlit cloud does not start 

## Aknowledgements

- We rely on `apimoex.ISSClient` and expertise developped within [apimoex project](https://github.com/WLM1ke/apimoex) by [@WLMike1](https://github.com/WLM1ke).
- Dividend history relayed from <https://github.com/WLM1ke/poptimizer>
