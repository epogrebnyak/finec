from finec.dividend import get_dividend_dataframe


def test_get_dividend_dataframe(tmp_path):
    filename = tmp_path / "div.csv"
    df = get_dividend_dataframe(str(filename))
    assert len(df) >= 2387
