from finec.dividend import get_dividend, get_dividend_all


def test_get_dividend_all(tmpdir):
    df1 = get_dividend_all(str(tmpdir), "div.csv", overwrite=False)
    assert len(df1) >= 2387


def test_get_dividend(tmpdir):
    df2 = get_dividend("AFLT", str(tmpdir), "div.csv", overwrite=True)
    assert len(df2) >= 3


def test_get_dividend_all_no_param():
    df = get_dividend_all()
    assert len(df) >= 2387
