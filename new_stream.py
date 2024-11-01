# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from math import cos, sin, pi

# Пример данных (замените на свои)
traty = pd.DataFrame({
    'Год': [2024, 2024, 2024, 2023, 2023, 2023],
    'Месяц': [7, 7, 6, 7, 6, 6],
    'Категория': ['Еда', 'Транспорт', 'Развлечения', 'Еда', 'Транспорт', 'Развлечения'],
    'Сумма': [5000, 3000, 2000, 4000, 2500, 1000]
})

# Функция для месячной таблицы и диаграммы
def traty_mes(year, month):
    traty_mesyc = traty[(traty['Год'] == year) & (traty['Месяц'] == month)] \
        .groupby('Категория')['Сумма'].sum() \
        .reset_index() \
        .sort_values('Сумма', ascending=False)
    
    traty_total = traty_mesyc['Сумма'].sum()
    traty_mesyc['Процент'] = (traty_mesyc['Сумма'] / traty_total) * 100

    # Построение круговой диаграммы с процентами
    plt.figure(figsize=(8, 6))
    wedges, texts = plt.pie(traty_mesyc['Сумма'], startangle=140, radius=1)
    
    for i, (wedge, row) in enumerate(zip(wedges, traty_mesyc.itertuples())):
        angle = (wedge.theta2 - wedge.theta1) / 2 + wedge.theta1
        x = 1.2 * cos(angle * pi / 180)
        y = 1.2 * sin(angle * pi / 180)
        plt.annotate(f"{row.Категория}: {row.Процент:.1f}%", xy=(x, y), xytext=(1.4 * x, 1.4 * y),
                     ha='center', va='center', fontsize=10, color='black',
                     arrowprops=dict(arrowstyle="-", color='gray'))

    #plt.suptitle(f"Распределение трат за {month}/{year}", fontsize=14, y=1.05)
    st.pyplot(plt)

    # Вывод таблицы без процентов и индекса
    st.write(traty_mesyc.drop(columns=['Процент']).reset_index(drop=True))
    #st.dataframe(traty_mesyc.drop(columns=['Процент']).reset_index(drop=True), use_container_width=True)

# Функция для годовой таблицы и диаграммы
def traty_god(year):
    traty_godic = traty[traty['Год'] == year] \
        .groupby('Категория')['Сумма'].sum() \
        .reset_index() \
        .sort_values('Сумма', ascending=False)
    
    traty_total = traty_godic['Сумма'].sum()
    traty_godic['Процент'] = (traty_godic['Сумма'] / traty_total) * 100

    # Построение круговой диаграммы с процентами
    plt.figure(figsize=(8, 6))
    wedges, texts = plt.pie(traty_godic['Сумма'], startangle=140, radius=1)
    
    for i, (wedge, row) in enumerate(zip(wedges, traty_godic.itertuples())):
        angle = (wedge.theta2 - wedge.theta1) / 2 + wedge.theta1
        x = 1.2 * cos(angle * pi / 180)
        y = 1.2 * sin(angle * pi / 180)
        plt.annotate(f"{row.Категория}: {row.Процент:.1f}%", xy=(x, y), xytext=(1.4 * x, 1.4 * y),
                     ha='center', va='center', fontsize=10, color='black',
                     arrowprops=dict(arrowstyle="-", color='gray'))

    #plt.suptitle(f"Распределение трат за {year}", fontsize=14, y=1.05)
    st.pyplot(plt)

    # Вывод таблицы без процентов и индекса
    st.write(traty_godic.drop(columns=['Процент']).reset_index(drop=True))
    #st.dataframe(traty_godic.drop(columns=['Процент']).reset_index(drop=True), use_container_width=True)

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
    st.header(f"Траты за {year}: {traty_total:,}".replace(",", " "))
    traty_god(year)
else:
    traty_mesyc = traty[(traty['Год'] == year) & (traty['Месяц'] == int(month))] \
        .groupby('Категория')['Сумма'].sum() \
        .reset_index() \
        .sort_values('Сумма', ascending=False)
    traty_total = traty_mesyc['Сумма'].sum()
    st.header(f"Траты за {month}/{year}: {traty_total:,}".replace(",", " "))
    traty_mes(year, int(month))
