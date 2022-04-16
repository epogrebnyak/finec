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
