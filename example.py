# pip install git+https://github.com/epogrebnyak/finec.git

from finec.moex import traded_boards, Market, dataframe, Index


ds = Index("IMOEX").composition()
tickers = [d["ticker"] for d in ds]

industries = dict(
    oilgas="GAZP LKOH SNGS SNGSP TATN TATNP NVTK TRNFP ROSN",
    retail="FIVE FIXP DSKY MAGN",
    mm="ALRS GMKN NLMK RUAL POLY CHMF PLZL POGR",
    finance="MOEX TCSG SBER SBERP VTBR CBOM",
    other="AFKS PIKK PHOR",
    transport="AFLT GLTR",
    technology="HHRU OZON YNDX VKCO",
    telecom="MTSS RTKM",
    power="HYDR IRAO FEES ENPG",
)
