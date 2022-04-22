from pathlib import Path

import bson
import pandas as pd
import requests


def save_dividend(filepath: str):
    """Save dividend information from WLM1ke/poptimizer to a local *filepath* as CSV file.
    Data source: <https://github.com/WLM1ke/poptimizer/tree/master/dump/source>
    Columns: `ticker`, `date`, `dividends`, `currency`.
    """
    url_div = "https://github.com/WLM1ke/poptimizer/blob/master/dump/source/dividends.bson?raw=true"
    if Path(filepath).exists():
        raise FileExistsError(f"File {filepath} already exists, will not overwrite.")
    r = requests.get(url_div)
    gen = bson.decode_iter(r.content)
    pd.DataFrame(gen).drop(columns=["_id"]).to_csv(filepath, index=False)


def get_dividend_dataframe(filepath: str) -> pd.DataFrame:
    """Return dividend information from WLM1ke/poptimizer as dataframe.

    Will read from local *filepath*, if exists, or download and save
    data to *filepath*, if it does not exist.

    Example:

      div_df = get_dividend_dataframe("dividend.csv")
      div_df[div_df.ticker=="GMKN"].sort_values("date", ascending=True)

    """
    if not Path(filepath).exists():
        save_dividend(filepath)
    return pd.read_csv(filepath, parse_dates=["date"])
