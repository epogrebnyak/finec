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


def to_dataframe(d):
    return pd.DataFrame(d)
