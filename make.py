import itertools

from finec.moex import Index, Stock, save_generator, yield_fields

# runs several minutes
tickers = Index("IMOEX").tickers()
gen = yield_fields(Stock, tickers, "CLOSE")
save_generator("datasets/IMOEX_CLOSE.csv", gen, "CLOSE")
