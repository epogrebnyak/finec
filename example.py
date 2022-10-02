# %% [markdown]
#
# # Основные вопросы
#
# 1. Данные по каким типам (классам) ценных бумаг доступны?
# 2. Как получить список тикеров по выбранному типу ценных бумаг?
# 3. Как получить котировки по всем тикерам за последний торговый день?
# 4. Как получить историю котировок по тикеру?
#

# %% [markdown]
#
# # А. Иерархия представления информации в API MOEX
#
# ```Engine -> Market -> Board````
#

# %%
from finec.moex import (
    BOARDS,
    CURRENCIES,
    MARKETS,
    Board,
    Engine,
    Market,
    bond_prices,
    bond_yields,
    corporate_bonds_board,
    get_engines,
    stock_prices,
    stocks_board,
    whoami,
)

#%%
# Какие торговые системы (engines) существуют на бирже?
for e in get_engines():
    print(e)


# %%
# Какие рынки (markets) есть для торговой системы ("движка") "stock"?
Engine("stock").markets()

# %%
# Выберем в торговой системе "stock" рынок акций ("shares")
m = Market(engine="stock", market="shares")
m

# %%
#
m.boards()[:10]

# %%
m.volumes()

# %%
m.securities().sample(3).set_index("SECID").T.dropna()

# %%
m.securities().SECID.unique().tolist()[:10]

# %%
# list available tickers - same as above
tickers = m.tickers()
len(tickers), tickers[:10]

# %%
from random import choice

t = choice(tickers)
whoami(t)


# %%
m.board("TQBR")

# %%
b = stocks_board("TQBR")

# %%
b = Board(engine="stock", market="shares", board="TQBR")
b

# %%
# Котитировки акций
def stocks_dafaframe():
    b = stocks_board()
    return stock_prices(b)


stocks_df = stocks_dafaframe().set_index("SECID", drop=True)[["CLOSE", "VALUE"]]

# %%
# Котитировки b
def bonds_dataframe():
    b = corporate_bonds_board()
    df = bond_prices(b).query("VOLUME>0")
    return df.merge(bond_yields(b), how="left", on="SECID")


bonds_df = bonds_dataframe()

# %%
from finec.moex import Bond, Index, Stock

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

# Sistema 2027 bond price and yields from TQCB trading bord
Bond(ticker="RU000A0JXN21", board="TQCB").get_history()

# What data columns are provided for trading history?
Bond(ticker="RU000A101NJ6", board="TQIR").provided_columns()


# %%
from finec.moex import CURRENCIES

CURRENCIES
# %%

from finec.yield_curve import YieldCurve, get_yields_from_cbr

y = YieldCurve("2022-09-28")
r1 = y.rate(t=1)
# 830.2383903307176

rs = get_yields_from_cbr("2022-09-28")
# {'0.25': 8.2, '0.50': 8.19, '0.75': 8.23, '1.00': 8.3, '2.00': 8.74, '3.00': 9.22, '5.00': 9.91, '7.00': 10.27, '10.00': 10.5, '15.00': 10.69, '20.00': 10.8, '30.00': 10.9}

# %%
