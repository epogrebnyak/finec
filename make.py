import itertools

from finec.moex import Index, Stock, save_generator, yield_fields
from finec.dividend import get_dividend_all

# create dividend file
get_dividend_all(temp_dir="datasets", temp_filename="dividend.csv", overwrite=True)

# create IMOEX quotes - runs several minutes
tickers = Index("IMOEX").tickers()
gen = yield_fields(Stock, tickers, "CLOSE")
save_generator("datasets/IMOEX_CLOSE.csv", gen, "CLOSE")
