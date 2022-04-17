from finec import moex


def test_start():
    assert moex.start() == 1


def test_find_systema_bond():  # will expire
    assert moex.find("СистемБ1P6") == [
        {
            "emitent_id": 2046,
            "emitent_inn": "7703104630",
            "emitent_okpo": "27987276",
            "emitent_title": 'Публичное акционерное общество "Акционерная финансовая корпорация "Система"',
            "gosreg": "4B02-06-01669-A-001P",
            "group": "stock_bonds",
            "id": 125886,
            "is_traded": 1,
            "isin": "RU000A0JXN21",
            "marketprice_boardid": "TQCB",
            "name": 'АФК "Система" ПАО БО-001P-06',
            "primary_boardid": "TQCB",
            "regnumber": "4B02-06-01669-A-001P",
            "secid": "RU000A0JXN21",
            "shortname": "СистемБ1P6",
            "type": "exchange_bond",
        }
    ]


def test_find_rusal_plant(): # not traded
    assert moex.find("Саяногорский") == [
        {
            "id": 86531,
            "secid": "oksa",
            "shortname": 'АО "РУСАЛ Саяногорск"',
            "regnumber": "1-02-40208-F",
            "name": 'Акционерное общество "РУСАЛ Саяногорский Алюминиевый Завод"',
            "isin": "RU0006936150",
            "is_traded": 0,
            "emitent_id": 487399,
            "emitent_title": 'Акционерное общество "РУСАЛ Саяногорский Алюминиевый Завод"',
            "emitent_inn": "1902014500",
            "emitent_okpo": None,
            "gosreg": "1-02-40208-F",
            "type": "common_share",
            "group": "stock_shares",
            "primary_boardid": "MXBD",
            "marketprice_boardid": None,
        }
    ]


def test_history_url():
    assert (
        moex.qualified(moex.history_endpoint("stock", "bonds", "TQCB", "RU000A0JTB96"))
        == "https://iss.moex.com/iss/history/engines/stock/markets/bonds/boards/TQCB/securities/RU000A0JTB96.json"
    )


def test_stock_history():
    assert moex.stock_history(
        security="MGNT",
        board="TQBR",
        columns=["SECID", "BOARDID", "TRADEDATE", "CLOSE", "VOLUME"],
        start="2021-11-15",
        end="2021-11-16",
    ) == [
        {
            "SECID": "MGNT",
            "BOARDID": "TQBR",
            "TRADEDATE": "2021-11-15",
            "CLOSE": 6499.5,
            "VOLUME": 396331,
        },
        {
            "SECID": "MGNT",
            "BOARDID": "TQBR",
            "TRADEDATE": "2021-11-16",
            "CLOSE": 6551,
            "VOLUME": 304449,
        },
    ]


def test_bond_history():
    assert moex.bond_history(
        security="RU000A101NJ6",
        board="TQIR",
        columns=["SECID", "BOARDID", "TRADEDATE", "CLOSE", "YIELDCLOSE", "MATDATE"],
        start="2022-04-15",
        end="2022-04-15",
    ) == [
        {
            "SECID": "RU000A101NJ6",
            "BOARDID": "TQIR",
            "TRADEDATE": "2022-04-15",
            "CLOSE": 79.5,
            "YIELDCLOSE": 23.05,
            "MATDATE": "2025-05-08",
        }
    ]
