from finec.moex import to_csv, Stock, Index

tickers = Index("IMOEX").tickers()

# runs several minutes
to_csv("datasets/IMOEX_CLOSE.csv", Stock, tickers, "CLOSE")
