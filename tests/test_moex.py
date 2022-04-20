from finec import moex


def find_by_secid():  # will expire
    assert moex.find("RU000A101NJ6") == [
        {
            "id": 384526849,
            "secid": "RU000A101NJ6",
            "shortname": "ЧЗПСНП БП2",
            "regnumber": "4B02-02-45194-D-001P",
            "name": "ЧЗПСН-Профнастил ПАО БО-П02",
            "isin": "RU000A101NJ6",
            "is_traded": 1,
            "emitent_id": 2578,
            "emitent_title": 'Публичное акционерное общество "Челябинский завод профилированного стального настила"',
            "emitent_inn": "7447014976",
            "emitent_okpo": "01217836",
            "gosreg": "4B02-02-45194-D-001P",
            "type": "exchange_bond",
            "group": "stock_bonds",
            "primary_boardid": "TQIR",
            "marketprice_boardid": "TQIR",
        }
    ]


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


def test_find_rusal_plant():  # not traded
    assert moex.find("Саяногорский", is_traded=False) == [
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


def test_provoded_columns():
    assert moex.Stock("YNDX").provided_columns() == [
        "BOARDID",
        "TRADEDATE",
        "SHORTNAME",
        "SECID",
        "NUMTRADES",
        "VALUE",
        "OPEN",
        "LOW",
        "HIGH",
        "LEGALCLOSEPRICE",
        "WAPRICE",
        "CLOSE",
        "VOLUME",
        "MARKETPRICE2",
        "MARKETPRICE3",
        "ADMITTEDQUOTE",
        "MP2VALTRD",
        "MARKETPRICE3TRADESVALUE",
        "ADMITTEDVALUE",
        "WAVAL",
        "TRADINGSESSION",
    ]


def test_stock_endpoint():
    assert (
        moex.qualified(moex.Stock("YNDX").history_endpoint)
        == "https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/YNDX.json"
    )


def test_stock_history_dataframe():
    import pandas as pd
    
    df = moex.Stock("YNDX").get_history(start="2022-01-15")
    assert isinstance(df, pd.DataFrame)
    assert len(df) >= 65


def test_stock_history():
    assert moex.Stock(ticker="MGNT", board="TQBR").get_history_json(
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
    assert moex.Bond(ticker="RU000A101NJ6", board="TQIR").get_history_json(
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


def test_whoami():
    assert moex.Bond("RU000A0JXN21").whoami() == {
        "SECID": "RU000A0JXN21",
        "NAME": 'АФК "Система" ПАО БО-001P-06',
        "SHORTNAME": "СистемБ1P6",
        "REGNUMBER": "4B02-06-01669-A-001P",
        "ISIN": "RU000A0JXN21",
        "ISSUEDATE": "2017-04-07",
        "MATDATE": "2027-03-26",
        "BUYBACKDATE": "2023-03-31",
        "INITIALFACEVALUE": "1000",
        "FACEUNIT": "SUR",
        "LATNAME": "AFK Systema 001P-06",
        "STARTDATEMOEX": "2017-04-07",
        "PROGRAMREGISTRYNUMBER": "4-01669-A-001P-02E",
        "EARLYREPAYMENT": "1",
        "LISTLEVEL": "2",
        "DAYSTOREDEMPTION": "1801",
        "ISSUESIZE": "15000000",
        "FACEVALUE": "1000",
        "ISQUALIFIEDINVESTORS": "0",
        "COUPONFREQUENCY": "2",
        "COUPONDATE": "2022-09-30",
        "COUPONPERCENT": "17",
        "COUPONVALUE": "84.77",
        "TYPENAME": "Биржевая облигация",
        "GROUP": "stock_bonds",
        "TYPE": "exchange_bond",
        "GROUPNAME": "Облигации",
        "EMITTER_ID": "2046",
    }


def test_traded_boards():
    assert list(moex.traded_boards("AFLT").keys()) == [
        "TQBR",
        "SPEQ",
        "SMAL",
        "TQDP",
        "RPMO",
        "PTEQ",
        "PSEQ",
        "RPEU",
        "RPEO",
        "EQRD",
        "EQRE",
        "EQWP",
        "EQWD",
        "EQWE",
        "EQRP",
        "LIQR",
        "EQRY",
        "PSRY",
        "PSRP",
        "PSRD",
        "PSRE",
        "LIQB",
    ]


def test_market_traded_boards():
    assert list(moex.Market("stock", "shares").traded_boards().keys()) == [
        "SMAL",
        "SPEQ",
        "TQBR",
        "TQDP",
        "TQFD",
        "TQFE",
        "TQIF",
        "TQPD",
        "TQPE",
        "TQPI",
        "TQTD",
        "TQTE",
        "TQTF",
    ]


def test_currency_history():
    assert moex.Currency("EUR_RUB__TOM", board="CETS").get_history_json(
        columns=None, start="2022-04-01", end="2022-04-01"
    ) == [
        {
            "BOARDID": "CETS",
            "TRADEDATE": "2022-04-01",
            "SHORTNAME": "EURRUB_TOM",
            "SECID": "EUR_RUB__TOM",
            "OPEN": 92.5,
            "LOW": 92.0375,
            "HIGH": 93.4675,
            "CLOSE": 92.99,
            "NUMTRADES": 5084,
            "VOLRUR": 37229929467.5,
            "WAPRICE": 92.5572,
        }
    ]


def test_index_history():
    assert moex.Index("IMOEX").get_history_json(start="2022-04-01", end="2022-04-01") == [
        {
            "BOARDID": "SNDX",
            "SECID": "IMOEX",
            "TRADEDATE": "2022-04-01",
            "SHORTNAME": "Индекс МосБиржи",
            "NAME": "Индекс МосБиржи",
            "CLOSE": 2759.64,
            "OPEN": 2714.62,
            "HIGH": 2817.72,
            "LOW": 2714.62,
            "VALUE": 77972322862.8,
            "DURATION": 0,
            "YIELD": 0,
            "DECIMALS": 2,
            "CAPITALIZATION": 13646014592832.201,
            "CURRENCYID": "RUB",
            "DIVISOR": 4944847155.0997,
            "TRADINGSESSION": "3",
            "VOLUME": None,
        }
    ]


def test_usd_rur():
    assert moex.usd_rur().get_history_json(start="2003-04-15", end="2003-04-15") == [
        {
            "BOARDID": "CETS",
            "TRADEDATE": "2003-04-15",
            "SHORTNAME": "USDRUB_TOM",
            "SECID": "USD000UTSTOM",
            "OPEN": 31.185,
            "LOW": 31.185,
            "HIGH": 31.1975,
            "CLOSE": 31.197,
            "NUMTRADES": 55,
            "VOLRUR": 1132583105,
            "WAPRICE": 31.1912,
        }
    ]


def test_index_composition():
    assert "SBER" in [d["ticker"] for d in moex.Index("IMOEX").composition()]
