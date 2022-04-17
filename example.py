from finec import moex

print(
    moex.bond_history(
        security="RU000A101NJ6",
        board="TQIR",
        columns=["SECID", "BOARDID", "TRADEDATE", "CLOSE", "YIELDCLOSE", "MATDATE"],
        start="2022-04-15",
        end="2022-04-15",
    )
)
