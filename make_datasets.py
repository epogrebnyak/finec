import itertools

from finec.dividend import get_dividend_all
from finec.moex import Index, Stock, save_tickers

# Create dividend file
get_dividend_all(directory="datasets", filename="dividend.csv", overwrite=True)

# Create IMOEX member company CLOSE prices - runs several minutes
save_tickers(
    path="datasets/IMOEX_CLOSE.csv",
    security_class=Stock,
    tickers=Index("IMOEX").tickers(),
    field="CLOSE",
)
