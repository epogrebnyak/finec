import streamlit as st

"""Демонстрация возможностей библиотеки finec:

- получить данные Московской биржи по акциям, облигациям или валютам
- преобразовать данные или объединить с данными из других источников
- построить графики
- записать в Excel

Все выполняется на основе [открытого кода](https://github.com/epogrebnyak/finec). 
"""

st.header("Акции")

"""Какие акции входят в состав индекса Мосбиржи и с какими весами?"""

from finec.moex import Index
import pandas as pd

imoex_dict = Index("IMOEX").composition()
cols = "ticker shortnames weight".split()
imoex_df = pd.DataFrame(imoex_dict)[cols].sort_values("weight", ascending=False).reset_index(drop=True)
st.dataframe(imoex_df)

# TODO: "Скачать данные (CSV, Excel)"

"""Сколько компаний торгуется на Московской бирже?"""

"""По каким акциям идет наибольший объем торгов?"""

# Дата обновления



st.header("Облигации")

"""По каким облигациям идет наибольший объем торгов?"""

st.header("Как скачать эти данные")

# Create in tempdir
