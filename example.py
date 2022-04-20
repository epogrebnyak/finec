from finec import moex

print(
    moex.Bond(ticker="RU000A101NJ6", board="TQIR").get_history(
        ["SECID", "BOARDID", "TRADEDATE", "CLOSE", "YIELDCLOSE", "MATDATE"]
    )
)
