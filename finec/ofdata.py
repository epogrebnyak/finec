# https://ofdata.ru/api/finances
from dataclasses import dataclass

import httpx


@dataclass
class Financials:
    api_key: str
    endpoint: str = "https://api.ofdata.ru/v2/finances"

    def get_json(self, **kwargs):
        params = dict(key=self.api_key)
        params.update(kwargs)
        return httpx.get(self.endpoint, params=params).json()

    def get_by_ogrn(self, ogrn: str, extended=False):
        if extended:
            return self.get_json(ogrn=ogrn, extended=True)
        else:
            return self.get_json(ogrn=ogrn)

    def get_by_inn(self, inn: str, kpp: str = "", extended=False):
        kwargs = dict(inn=inn)
        if kpp:
            kwargs["kpp"] = kpp
        if extended:
            kwargs["extended"] = True
        return self.get_json(**kwargs)


if __name__ == "__main__":
    # NEXT: use https://requests-cache.readthedocs.io/en/stable/
    import pathlib
    from pathlib import Path

    from dotenv import get_key, load_dotenv

    file = Path(__file__).parent / "ofdata.env"
    env_text = file.read_text()
    api_key = get_key(str(file), "OFDATA_APIKEY")
    a = Financials(api_key).get_by_inn("8401005730")
    print(a)
