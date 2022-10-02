from finec.yield_curve import Y, yield_curve, get_yields_from_cbr, make_date, YieldCurve

params = {
    "tradedate": "2022-09-28",
    "tradetime": "18:39:57",
    "b1": 1054.712544,
    "b2": -259.871694,
    "b3": -358.166406,
    "t1": 0.9689,
    "g1": -0.059222,
    "g2": 3.069814,
    "g3": -2.954618,
    "g4": -3.687879,
    "g5": 8.935729,
    "g6": 0.733885,
    "g7": 0.658087,
    "g8": 0.0,
    "g9": 0.0,
}


def test_Y():
    assert round(Y(1, params), 2) == 830.24


def test_yield_curve():
    assert round(yield_curve("2022-09-28", 1), 2) == 830.24


def test_YieldCurve():
    assert round(YieldCurve("2022-09-28").rate(t=1), 2) == 830.24


def test_make_date():
    assert make_date("2022-09-28") == "28.09.2022"


def test_get_yields_from_cbr():
    assert get_yields_from_cbr("2022-09-28") == {
        "0.25": 8.2,
        "0.50": 8.19,
        "0.75": 8.23,
        "1.00": 8.3,
        "2.00": 8.74,
        "3.00": 9.22,
        "5.00": 9.91,
        "7.00": 10.27,
        "10.00": 10.5,
        "15.00": 10.69,
        "20.00": 10.8,
        "30.00": 10.9,
    }
