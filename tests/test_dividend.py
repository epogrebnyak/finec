from finec.dividend import get_dividend_dataframe


def test_get_dividend_dataframe(tmp_path):
    filename = str(tmp_path / "div.csv")
    df = get_dividend_dataframe(temp_filepath=filename)
    assert len(df) >= 2387
