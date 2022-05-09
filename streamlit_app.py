import altair as alt
import pandas as pd
import streamlit as st

from finec.moex import (
    Index,
    Stock,
    industry,
    whoami,
    corporate_bonds,
    bond_yields,
)

st.title("Акции, облигации и валюта - данные Московской биржи")

#  Больше дат и номеров версий

"""
[finec]: https://github.com/epogrebnyak/finec

[![package version](https://badgen.net/pypi/v/finec)][finec]
"""

with st.expander("Комментарии", expanded=False):
  """Что умеем делать:

- получать данные Московской биржи по акциям, облигациям или валютам 
  в машинночитаемом виде
- строить графики 
- предоставить данные для скачивания в формате CSV

Что хотим делать:

- объединить с данными из других источников (например, финансовая отчетность и макро)
- данные зарубежных бирж
- примеры в ноутбуке Google Colab 
- контрольные вопросы для студентов
- больше ссылкок на зеркальные страницы Мосбиржи

Как работает:

- выполняется на основе [открытого кода библиотеки finec][finec]
- использует открытые данные Мосбиржи ([ISS MOEX](https://www.moex.com/a2193))
- показываем эту страницу через Streamlit Cloud

Что добавить или изменить?

- напишите мне в [ишью](https://github.com/epogrebnyak/finec/issues).
"""


def button_donwload_csv(df, filename="file.csv"):
    st.download_button(
        "Скачать данные (CSV)",
        df.to_csv().encode("utf-8"),
        filename,
        "text/csv",
        key="download-csv",
    )


st.header("Акции")

st.subheader("Какие акции входят в состав индекса Мосбиржи и с какими весами?")


@st.cache
def composition_df() -> pd.DataFrame:
    gen = Index("IMOEX").composition()
    cols = "ticker shortnames weight".split()
    df = (
        pd.DataFrame(gen)[cols]
        .sort_values("weight", ascending=False)
        .reset_index(drop=True)
    )
    df.index += 1
    df["industry"] = df.ticker.map(industry)
    return df


imoex_df = composition_df()

n_companies = st.slider(
    "Выберите количество компаний:",
    min_value=1,
    max_value=len(imoex_df),
    value=15,
    step=1,
)
if n_companies < len(imoex_df):
    pct = imoex_df.iloc[:n_companies, :].weight.sum()
    st.write(
        f"Крупнейшие по капитализации {n_companies} компаний "
        f"составляют {pct:.1f}% индекса Московской биржи."
    )
else:
    st.write(f"В состав индекса Московской биржи входят {len(imoex_df)} компании.")

c = (
    alt.Chart(imoex_df.iloc[:n_companies, :])
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
button_donwload_csv(imoex_df, "imoex.csv")

st.subheader("Как получить котировки акции по тикеру")

#    - Показать дивиденды
#    - Показать последние цены и обороты
#    - Сравнить с индексом Мосбиржи

random_tickers = sorted(imoex_df.sample(5).ticker.to_list())
st.write("Примеры тикеров:", ", ".join(random_tickers))

ticker = st.text_input("Введите тикер и нажмите Enter:")
if ticker:
    s = Stock(ticker)
    desc_dict = s.whoami()
    st.write(desc_dict["TYPENAME"], desc_dict["NAME"])
    ticker_df = s.get_history()
    st.line_chart(ticker_df["CLOSE"])
    button_donwload_csv(ticker_df, "ticker.csv")

"""Исторические данные по котировкам акций индекса Мосбиржи за 2013-2022 гг. 
   можно также [скачать здесь.](https://raw.githubusercontent.com/epogrebnyak/finec/main/datasets/IMOEX_CLOSE.csv)
"""

st.header("Облигации")

#№with st.expander("Что добавить"):
#    """
#    - Нарисовать график цен и доходности отдельной облигации
#    - Указывать на нем события
#    - Нарисовать график доходности отдельной облигации
#    """

st.subheader("Кривая доходности корпоративных облигаций")

# Убрать несуществующие облигации
# Добавить график доходностей и цен облигаций

@st.cache
def bond_yields_dafaframe():
    b = corporate_bonds()
    return bond_yields(b)

bonds_df = bond_yields_dafaframe()

c2 = (
    alt.Chart(bonds_df.query("TERM < 15").query("0 < EFFECTIVEYIELD < 60"))
    .mark_circle(size=60)
    .encode(
        x=alt.X(
            "TERM",
            scale=alt.Scale(domain=(0, 15)),
            axis=alt.Axis(title="Лет до погашения или оферты (TERM)"),
        ),
        y=alt.Y(
            "EFFECTIVEYIELD",
            scale=alt.Scale(domain=(0, 60)),
            axis=alt.Axis(title="Доходность, % годовых (EFFECTIVEYIELD)"),
        ),
        tooltip=["SECID", "EFFECTIVEYIELD", "TERM"],
    )
    .configure_mark(opacity=0.2)
)

st.altair_chart(c2, use_container_width=True)
button_donwload_csv(bonds_df, "yields.csv")
