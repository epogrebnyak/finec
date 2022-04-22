import itertools
from finec.moex import save_generator, yield_fields, Stock, Index

# runs several minutes
tickers = Index("IMOEX").tickers()
gen = yield_fields(Stock, tickers, "CLOSE")
save_generator("datasets/IMOEX_CLOSE.csv", gen, "CLOSE")
