class ValidColumns:
    security_bond = [  # security
        "SECID",
        "SECNAME",
        "SHORTNAME",
        "LATNAME",
        "BOARDID",
        "BOARDNAME",
        "LISTLEVEL",
        "STATUS",
        "ISIN",
        "REGNUMBER",
        "MARKETCODE",
        "INSTRID",
        "SECTORID",
        "SECTYPE",
        "CURRENCYID",
        "DECIMALS",
        "MINSTEP",
        "LOTSIZE",
        "LOTVALUE",
        "FACEUNIT",
        "FACEVALUE",
        "ISSUESIZE",
        "ISSUESIZEPLACED",
        "REMARKS",
        # latest quote
        "OFFERDATE",
        "MATDATE",
        "BUYBACKDATE",
        "BUYBACKPRICE",
        "COUPONPERCENT",
        "COUPONVALUE",
        "COUPONPERIOD",
        "NEXTCOUPON",
        "ACCRUEDINT",
        "SETTLEDATE",
        "PREVDATE",
        "PREVPRICE",
        "YIELDATPREVWAPRICE",
    ]

    security_currency = [
        "SECID",
        "BOARDID",
        "MARKETCODE",
        "SECNAME",
        "SHORTNAME",
        "SETTLEDATE",
        "PREVPRICE",
        "PREVWAPRICE",
        "PREVDATE",
        "CURRENCYID",
    ]

    history_bond = [
        "TRADEDATE",
        "BOARDID",
        "HIGH",
        "LOW",
        "OPEN",
        "CLOSE",
        "WAPRICE",
        "YIELDCLOSE",
        "NUMTRADES",
        "VALUE",
        "VOLUME",
        "MATDATE",
        "OFFERDATE",
        "BUYBACKDATE",
        "DURATION",
        "COUPONPERCENT",
        "COUPONVALUE",
        "ACCINT",
        "FACEVALUE",
        "FACEUNIT",
        "CURRENCYID",
    ]

    history_stock = [
        "TRADEDATE",
        "BOARDID",
        "HIGH",
        "LOW",
        "OPEN",
        "CLOSE",
        "WAPRICE",
        "NUMTRADES",
        "VALUE",
        "VOLUME",
    ]
