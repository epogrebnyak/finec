# pip install git+https://github.com/epogrebnyak/finec.git

from finec.moex import traded_boards, Market, dataframe

# m = Market("stock", "shares")
# m = Market("stock", "bonds")
# sec = m.securities()

from finec.dividend import get_dividend_all

div_df = get_dividend_all()
