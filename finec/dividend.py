from pathlib import Path

import appdirs
import bson
import pandas as pd
import requests


def query_dividend_from_web() -> pd.DataFrame:
    url_div = "https://github.com/WLM1ke/poptimizer/blob/master/dump/source/dividends.bson?raw=true"
    r = requests.get(url_div)
    gen = bson.decode_iter(r.content)
    return pd.DataFrame(gen).drop(columns=["_id"])


def save(df, filepath: str, overwrite=False):
    df.to_csv(filepath, index=False)


def read(filepath):
    return pd.read_csv(filepath, parse_dates=["date"])


def cache_factory(from_web, to_file, from_file, default_filename):
    def f(temp_filename: str, temp_dir: str, overwrite: bool = False):
        if not temp_dir:
            temp_dir = Path(appdirs.user_cache_dir())
        if not Path(temp_dir).exists():
            raise FileNotFoundError(f"{temp_dir} does not exist.")
        if not temp_filename:
            temp_filename = default_filename
        filepath = Path(temp_dir) / temp_filename
        if overwrite or not filepath.exists():
            df = from_web()
            to_file(df, filepath)
        return from_file(filepath)

    return f


def get_dividend_all(
    temp_dir: str = "", temp_filename: str = "", overwrite: bool = False
):
    return get_dividend(None, temp_dir, temp_filename, overwrite)


def get_dividend(
    ticker="", temp_dir: str = "", temp_filename: str = "", overwrite: bool = False
):
    """Return dividend information from WLM1ke/poptimizer as dataframe.
       Subset by *ticker*, if *ticker* is provided.

    Caching:
      - Uses cached data *temp_dir/temp_filename*.
      - Will read from local *temp_dir/temp_filename*, if exists.
      - If *temp_dir/temp_filename* does not exist will download data
        and save it to *temp_dir/temp_filename*.
      - Same behaviour if `overwrite=True`.

    Example:

       get_dividend("GMKN")

    Data source: <https://github.com/WLM1ke/poptimizer/tree/master/dump/source>
    Columns: `ticker`, `date`, `dividends`, `currency`.
    """
    f = cache_factory(
        from_web=query_dividend_from_web,
        to_file=save,
        from_file=read,
        default_filename="moex_dividend.csv",
    )
    df = f(temp_filename, temp_dir, overwrite)
    if ticker:
        df = df[df.ticker == ticker].sort_values("date", ascending=True)
    return df
