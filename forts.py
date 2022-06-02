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
