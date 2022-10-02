#%%
from pathlib import Path

import bson
import pandas as pd
import requests

from finec.directory import local_directory

DIVIDEND_URL = "https://github.com/WLM1ke/poptimizer/blob/master/dump/data_new/raw_div.bson?raw=true"


def yield_dividends(url=DIVIDEND_URL):
    r = requests.get(url)
    for item in bson.decode_iter(r.content):
        ticker = item["_id"]
        for div in item["df"]:
            div["ticker"] = ticker
            yield div


def query_dividend_from_web(url=DIVIDEND_URL) -> pd.DataFrame:
    gen = yield_dividends(url)
    return pd.DataFrame(gen)


def save(df, filepath: str):
    df.to_csv(filepath, index=False)


def read(filepath):
    return pd.read_csv(filepath, parse_dates=["date"])


def default_filepath():
    return local_directory() / "dividend.csv"


def get_dividend_all(filepath: str = ""):
    if filepath == "":
        path = default_filepath()
    else:
        path = Path(filepath)
    if path.exists():
        return read(path)
    else:
        df = query_dividend_from_web()
        save(df, path)
        return df

#%%

get_dividend_all("")


#%%
def erase_local_file():
    # FIXME: must delete default_filepath().
    pass


def get_dividend(ticker: str, filepath: str = ""):
    """Return dividend for *ticker* from WLM1ke/poptimizer as dataframe.

    Caching:
      - Uses cached data at *filepath*. Will read from *filepath*, if exists.
      - If *filepath* does not exist will download data and save it to *filepath*.
      - Uses default location otherwise.

    Example:

       get_dividend("GMKN")

    Data source: <https://github.com/WLM1ke/poptimizer/tree/master/dump/source>
    Columns: `ticker`, `date`, `dividends`, `currency`.
    """
    df = get_dividend_all(filepath)
    return df[df.ticker == ticker].sort_values("date", ascending=True)
