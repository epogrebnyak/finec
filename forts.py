#%%
from finec.moex import Market, whoami, find, Board, Security, default, ClassList

#%%
find("Si-6.22")

#%%
whoami("SiM2")

#%%
Market(engine="futures", market="forts").traded_boards()

#%%
b = Board(engine="futures", market="forts", board="RFUD")

# %%
from dataclasses import dataclass


@dataclass
class Futures(Security):
    ticker: str
    board: str = "RFUD"
    engine: str = default("futures")
    market: str = default("forts")
    default_columns: ClassList = []


#%%
Futures("SiM2").get_history().dropna()

#%%
from finec.moex import get_engines, Board, Engine, Market

for e in get_engines():
    for m in Engine(e).markets():
        for b_name in Market(e, m).traded_boards():
            b = Board(e, m, b_name)
            v = b.volume()
            if v:
               print(b, v)
               b.__dict__

# need: Board.volume()

# %%
