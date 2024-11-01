# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from math import cos, sin, pi, ceil

# Пример данных (замените на свои)
sheet_id = "1-rxT9EY-rCqRbO_cNwngIcr1Z0qDgmr4dvyY-LXPkv4"
traty = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
traty['Сумма'] = traty['Сумма'].str.replace(',', '.')
traty['Сумма']=traty['Сумма'].astype('float')

# Функция для месячной таблицы и диаграммы
def traty_mes(year, month):
    traty_mesyc = traty[(traty['Год'] == year) & (traty['Месяц'] == month)] \
        .groupby('Категория')['Сумма'].sum() \
        .reset_index() \
        .sort_values('Сумма', ascending=False)
    
    traty_total = traty_mesyc['Сумма'].sum()
    traty_mesyc['Процент'] = (traty_mesyc['Сумма'] / traty_total) * 100
    
    # Ограничение категорий с долей менее 5%
    traty_mesyc_above_5 = traty_mesyc[traty_mesyc['Процент'] >= 5]
    other_sum = traty_mesyc[traty_mesyc['Процент'] < 5]['Сумма'].sum()
    
    # Добавляем категорию "Другие" для категорий с долей менее 5%
    if other_sum > 0:
        traty_mesyc_above_5 = pd.concat([traty_mesyc_above_5, pd.DataFrame({'Категория': ['Другие'], 'Сумма': [other_sum], 'Процент': [other_sum / traty_total * 100]})])

    # Построение круговой диаграммы с процентами
    plt.figure(figsize=(8, 6))
    wedges, texts = plt.pie(traty_mesyc_above_5['Сумма'], startangle=140, radius=1)
    
    for i, (wedge, row) in enumerate(zip(wedges, traty_mesyc_above_5.itertuples())):
        angle = (wedge.theta2 - wedge.theta1) / 2 + wedge.theta1
        x = 1.2 * cos(angle * pi / 180)
        y = 1.2 * sin(angle * pi / 180)
        plt.annotate(f"{row.Категория}: {row.Процент:.1f}%", xy=(x, y), xytext=(1.4 * x, 1.4 * y),
                     ha='center', va='center', fontsize=10, color='black',
                     arrowprops=dict(arrowstyle="-", color='gray'))

    st.pyplot(plt)

    # Вывод таблицы без процентов и индекса
    st.dataframe(traty_mesyc_above_5.drop(columns=['Процент']).reset_index(drop=True).style.format({'Сумма': '{:.0f}'}).replace(",", " ")), use_container_width=False))

# Функция для годовой таблицы и диаграммы
def traty_god(year):
    traty_godic = traty[traty['Год'] == year] \
        .groupby('Категория')['Сумма'].sum() \
        .reset_index() \
        .sort_values('Сумма', ascending=False)
    
    traty_total = traty_godic['Сумма'].sum()
    traty_godic['Процент'] = (traty_godic['Сумма'] / traty_total) * 100
    
    # Ограничение категорий с долей менее 5%
    traty_godic_above_5 = traty_godic[traty_godic['Процент'] >= 5]
    other_sum = traty_godic[traty_godic['Процент'] < 5]['Сумма'].sum()
    
    # Добавляем категорию "Другие" для категорий с долей менее 5%
    if other_sum > 0:
        traty_godic_above_5 = pd.concat([traty_godic_above_5, pd.DataFrame({'Категория': ['Другие'], 'Сумма': [other_sum], 'Процент': [other_sum / traty_total * 100]})])

    # Построение круговой диаграммы с процентами
    plt.figure(figsize=(8, 6))
    wedges, texts = plt.pie(traty_godic_above_5['Сумма'], startangle=140, radius=1)
    
    for i, (wedge, row) in enumerate(zip(wedges, traty_godic_above_5.itertuples())):
        angle = (wedge.theta2 - wedge.theta1) / 2 + wedge.theta1
        x = 1.2 * cos(angle * pi / 180)
        y = 1.2 * sin(angle * pi / 180)
        plt.annotate(f"{row.Категория}: {row.Процент:.1f}%", xy=(x, y), xytext=(1.4 * x, 1.4 * y),
                     ha='center', va='center', fontsize=10, color='black',
                     arrowprops=dict(arrowstyle="-", color='gray'))

    st.pyplot(plt)

    # Вывод таблицы без процентов и индекса
    #st.write(traty_godic_above_5.drop(columns=['Процент']).reset_index(drop=True))
    st.dataframe(traty_godic_above_5.drop(columns=['Процент']).reset_index(drop=True).style.format({'Сумма': '{:.0f}'}).replace(",", " ")), use_container_width=False)

# Интерфейс Streamlit
st.sidebar.header("Параметры фильтрации")
year = st.sidebar.selectbox("Выберите год", sorted(traty['Год'].unique()))
month_options = ["Все месяцы"] + sorted(traty['Месяц'].unique())
month = st.sidebar.selectbox("Выберите месяц", month_options)

# Логика отображения данных в зависимости от выбора месяца
if month == "Все месяцы":
    traty_godic = traty[traty['Год'] == year] \
        .groupby('Категория')['Сумма'].sum() \
        .reset_index() \
        .sort_values('Сумма', ascending=False)
    traty_total = traty_godic['Сумма'].sum()
    st.header(f"Траты за {year}: {traty_total:,.0f}".replace(",", " "))
    traty_god(year)
else:
    traty_mesyc = traty[(traty['Год'] == year) & (traty['Месяц'] == int(month))] \
        .groupby('Категория')['Сумма'].sum() \
        .reset_index() \
        .sort_values('Сумма', ascending=False)
    traty_total = traty_mesyc['Сумма'].sum()
    st.header(f"Траты за {month}/{year}: {traty_total:,.0f}".replace(",", " "))
    traty_mes(year, int(month))
