from finec import moex


def test_start():
    assert moex.start() == 1


def test_find():
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
