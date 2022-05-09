import altair as alt
import pandas as pd
import streamlit as st

from finec.moex import Index, industry, whoami

st.title("Акции, облигации и валюта - данные Московской биржи")

"""
[finec]: https://github.com/epogrebnyak/finec

[![package version](https://badgen.net/pypi/v/finec)][finec]

Что умеем делать:

- получить данные Московской биржи по акциям, облигациям или валютам
- преобразовать данные и объединить их с данными из других источников
- построить графики 
- скачать данные в формате CSV

Как работает:

- выполняется на основе [открытого кода][finec]
- использует открытые данные Мосбиржи ([ISS MOEX](https://www.moex.com/a2193))
- можно повторить расчеты в ноутбуке Google Colab 

Какие данные, графики или функционал вы бы хотели здесь видеть?
Напишите в [ишью](https://github.com/epogrebnyak/finec/issues).
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
button_donwload_csv(imoex_df, "imoex.csv")

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
st.dataframe(imoex_df.iloc[:n_companies, :])

st.subheader("Узнать про тикер")

random_ticker = "IRAO"  # imoex_df.sample(1).ticker.iloc[0]
ticker = st.text_input("Введите тикер:", random_ticker)
if ticker:
    describe_dict = whoami(ticker)
    st.write(describe_dict["TYPENAME"], describe_dict["NAME"])
    with st.expander("Больше информации", expanded=False):
        st.write(describe_dict)


# """Сколько компаний торгуется на Московской бирже?"""

# """По каким акциям идет наибольший объем торгов?"""

# Дата обновления


# st.header("Облигации")

# """По каким облигациям идет наибольший объем торгов?"""
