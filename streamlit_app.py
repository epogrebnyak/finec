from example import industry
import streamlit as st
from finec.moex import Index, industry
import pandas as pd

"""Демонстрация возможностей библиотеки finec:

- получить данные Московской биржи по акциям, облигациям или валютам
- преобразовать данные или объединить с данными из других источников
- построить графики
- записать в Excel

Все выполняется на основе [открытого кода](https://github.com/epogrebnyak/finec). 
"""

st.header("Акции")

"""Какие акции входят в состав индекса Мосбиржи и с какими весами?"""


@st.cache
def composition_df() -> pd.DataFrame:
    return pd.DataFrame(Index("IMOEX").composition())


cols = "ticker shortnames weight".split()
imoex_df = (
    composition_df()[cols].sort_values("weight", ascending=False).reset_index(drop=True)
)
imoex_df.index += 1
imoex_df["industry"] = imoex_df.ticker.map(industry)

import altair as alt

c = (
    alt.Chart(imoex_df)
    .mark_bar()
    .encode(
        x="weight",
        y=alt.Y("ticker", sort="-x"),
        tooltip=["ticker", "weight"],
        color=alt.Color(
            "industry",
            legend=alt.Legend(title="Обозначения отраслей"),
            scale=alt.Scale(scheme="redblue"),
        ),
    )
)

st.altair_chart(c, use_container_width=True)

st.dataframe(imoex_df)

# TODO: "Скачать данные (CSV, Excel)"

"""Сколько компаний торгуется на Московской бирже?"""

"""По каким акциям идет наибольший объем торгов?"""

# Дата обновления


st.header("Облигации")

"""По каким облигациям идет наибольший объем торгов?"""

st.header("Как скачать эти данные")

# Create in tempdir
