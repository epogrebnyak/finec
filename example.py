# pip install git+https://github.com/epogrebnyak/finec.git

from finec.moex import traded_boards, Market, dataframe

# m = Market("stock", "shares")
m = Market("stock", "bonds")
sec = m.history()
