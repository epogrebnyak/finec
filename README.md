# finec

Financial data and computation for Finec MGIMO students.


## Installation

```console
pip install git+https://github.com/epogrebnyak/finec.git
```

## Minimal example

Get trading history by security:

```python
from finec.moex import Bond, Currency, Stock, dataframe

dataframe(Stock("YNDX").get_history(start="2022-01-01"))
dataframe(Bond(ticker="RU000A101NJ6", board="TQIR").get_history())
dataframe(Currency("USD000UTSTOM").get_history(start="20221-01-01"))
```