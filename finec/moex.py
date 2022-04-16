from apimoex import ISSClient
import requests
import pandas as pd


def start():
    return 1


def qualified(endpoint):
    assert endpoint.startswith("/iss")
    return "https://iss.moex.com" + endpoint + ".json"


def get(endpoint, param={}):
    with requests.Session() as session:
        return ISSClient(session, qualified(endpoint), param).get()


def get_all(endpoint, param={}):
    with requests.Session() as session:
        return ISSClient(session, qualified(endpoint), param).get_all()


def find(query_str: str):
    return get_all(endpoint="/iss/securities", param=dict(q=query_str))["securities"]


def history_url(engine, market, board, security):
    endpoint = (
        f"/iss/history/engines/{engine}"
        f"/markets/{market}"
        f"/boards/{board}/"
        f"securities/{security}"
    )
    return qualified(endpoint)


def board_quote(engine, market, board, security, param={}):
    endpoint = (
        f"/iss/history/engines/{engine}"
        f"/markets/{market}"
        f"/boards/{board}/"
        f"securities/{security}"
    )
    return get_all(endpoint, param)["history"]


def history_column_param(columns):
    return {"history.columns": ",".join(columns)}


class ValidColumns:
    security_bond = [  # security
        "SECID",
        "SECNAME",
        "SHORTNAME",
        "LATNAME",
        "BOARDID",
        "BOARDNAME",
        "LISTLEVEL",
        "STATUS",
        "ISIN",
        "REGNUMBER",
        "MARKETCODE",
        "INSTRID",
        "SECTORID",
        "SECTYPE",
        "CURRENCYID",
        "DECIMALS",
        "MINSTEP",
        "LOTSIZE",
        "LOTVALUE",
        "FACEUNIT",
        "FACEVALUE",
        "ISSUESIZE",
        "ISSUESIZEPLACED",
        "REMARKS",
        # latest quote
        "OFFERDATE",
        "MATDATE",
        "BUYBACKDATE",
        "BUYBACKPRICE",
        "COUPONPERCENT",
        "COUPONVALUE",
        "COUPONPERIOD",
        "NEXTCOUPON",
        "ACCRUEDINT",
        "SETTLEDATE",
        "PREVDATE",
        "PREVPRICE",
        "YIELDATPREVWAPRICE",
    ]

    history_bond = [
        "TRADEDATE",
        "BOARDID" "HIGH",
        "LOW",
        "OPEN",
        "CLOSE",
        "WAPRICE",
        "YIELDCLOSE",
        "NUMTRADES",
        "VALUE",
        "VOLUME",
        "MATDATE",
        "OFFERDATE",
        "BUYBACKDATE" "DURATION",
        "COUPONPERCENT",
        "COUPONVALUE",
        "ACCINT",
        "FACEVALUE",
        "FACEUNIT",
        "CURRENCYID",
    ]

    history_stock = [
        "TRADEDATE",
        "BOARDID" "HIGH",
        "LOW",
        "OPEN",
        "CLOSE",
        "WAPRICE",
        "NUMTRADES",
        "VALUE",
        "VOLUME",
    ]


def get_bonds():
    return get("/iss/engines/stock/markets/bonds/securities")["securities"]


def get_shares():
    return get("/iss/engines/stock/markets/shares/securities")["securities"]


def stock_history(security, board="TQBR", columns=ValidColumns.history_stock):
    param = {}
    if columns:
        param = history_column_param(columns)
    return board_quote("stock", "shares", board, security, param)


def bond_history(security, board="TQCB", columns=ValidColumns.history_bond):
    param = {}
    if columns:
        param = history_column_param(columns)
    return board_quote("stock", "bonds", board, security, param)


def as_date(s: str):
    try:
        return pd.Timestamp(s)
    except ValueError:
        return pd.NA


def dataframe(json_dict):
    df = pd.DataFrame(json_dict)
    if "TRADEDATE" in df.columns:
        df["TRADEDATE"] = pd.to_datetime(df["TRADEDATE"])
        df = df.set_index("TRADEDATE")
    date_cols = ["MATDATE", "OFFERDATE", "BUYBACKDATE"]
    for col in date_cols:
        if col in df.columns:
            df[col] = df[col].map(as_date)
    return df
