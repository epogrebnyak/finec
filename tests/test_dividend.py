from pathlib import Path
import pandas as pd

from finec.dividend import get_dividend, get_dividend_all
from finec.moex import Stock


def test_mounted_get_dividend():
    df = Stock("GMKN").get_dividend()
    assert isinstance(df, pd.DataFrame)
    assert len(df) >= 16


def test_get_dividend_all(tmpdir):
    df1 = get_dividend_all(Path(tmpdir) / "div.csv")
    assert len(df1) >= 2387


def test_get_dividend(tmpdir):
    df2 = get_dividend("AFLT", Path(tmpdir) / "div.csv")
    assert len(df2) >= 3


def test_get_dividend_all_no_param():
    df = get_dividend_all()
    assert len(df) >= 2387
