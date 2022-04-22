[![Tests](https://github.com/epogrebnyak/finec/actions/workflows/.pytest.yml/badge.svg)](https://github.com/epogrebnyak/finec/actions/workflows/.pytest.yml)

# finec

Financial data and computation for Finec MGIMO students.


## Installation

```console
pip install git+https://github.com/epogrebnyak/finec.git
```

## Minimal example

Get MOEX trading history for stocks, bonds or currencies as pandas dataframe:

```python
from finec.moex import Bond, Currency, Stock, Index

# Yandex stock price
Stock("YNDX").get_history()

# Sistema 2027 bond price and yields
Bond(ticker="RU000A0JXN21", board="TQCB").get_history()

# USDRUR exchange rate
Currency("USD000UTSTOM").get_history(start="2020-01-01")

# MOEX stock index
Index("IMOEX").get_history()
```

## More examples

See [example.py](example.py)


## Aknowledgements

- We rely on `apimoex.ISSClient` and expertise developped within [apimoex project](https://github.com/WLM1ke/apimoex) by [@WLMike1](https://github.com/WLM1ke).

