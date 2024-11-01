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

st.sidebar.header("Параметры фильтрации")

# Множественный выбор для годов и месяцев, включая возможность выбрать "Все года" и "Все месяцы"
year_options = ["Все года"] + sorted(traty['Год'].unique())
selected_years = st.sidebar.multiselect("Выберите годы", year_options, default="Все года")

month_options = ["Все месяцы"] + sorted(traty['Месяц'].unique())
selected_months = st.sidebar.multiselect("Выберите месяцы", month_options, default="Все месяцы")

# Логика фильтрации в зависимости от выбранных годов и месяцев
if "Все года" in selected_years:
    # Если выбраны "Все года"
    if "Все месяцы" in selected_months:
        # Все года и все месяцы
        traty_filtered = traty
        traty_total = traty_filtered['Сумма'].sum()
        st.header(f"Траты за все года: {traty_total:,.0f}".replace(",", " "))
    else:
        # Все года и выбранные месяцы
        traty_filtered = traty[traty['Месяц'].isin([int(m) for m in selected_months])]
        traty_total = traty_filtered['Сумма'].sum()
        st.header(f"Траты за все года, месяцы {', '.join(map(str, selected_months))}: {traty_total:,.0f}".replace(",", " "))
else:
    # Выбран конкретный год или несколько годов
    filtered_years = [int(year) for year in selected_years]
    if "Все месяцы" in selected_months:
        # Конкретные годы и все месяцы
        traty_filtered = traty[traty['Год'].isin(filtered_years)]
        traty_total = traty_filtered['Сумма'].sum()
        st.header(f"Траты за годы {', '.join(map(str, filtered_years))}: {traty_total:,.0f}".replace(",", " "))
    else:
        # Конкретные годы и выбранные месяцы
        traty_filtered = traty[(traty['Год'].isin(filtered_years)) & (traty['Месяц'].isin([int(m) for m in selected_months]))]
        traty_total = traty_filtered['Сумма'].sum()
        st.header(f"Траты за годы {', '.join(map(str, filtered_years))}, месяцы {', '.join(map(str, selected_months))}: {traty_total:,.0f}".replace(",", " "))

# Группировка и визуализация данных после фильтрации
traty_grouped = traty_filtered.groupby('Категория')['Сумма'].sum().reset_index().sort_values('Сумма', ascending=False)
traty_grouped['Процент'] = (traty_grouped['Сумма'] / traty_total) * 100

# Фильтрация категорий для отображения в круговой диаграмме (ограничение по проценту)
traty_above_5 = traty_grouped[traty_grouped['Процент'] >= 5]
other_sum = traty_grouped[traty_grouped['Процент'] < 5]['Сумма'].sum()

if other_sum > 0:
    traty_above_5 = pd.concat([traty_above_5, pd.DataFrame({
        'Категория': ['Другие'], 
        'Сумма': [other_sum], 
        'Процент': [other_sum / traty_total * 100]
    })])

# Построение круговой диаграммы
plt.figure(figsize=(8, 6))
wedges, texts = plt.pie(traty_above_5['Сумма'], startangle=140, radius=1)

for i, (wedge, row) in enumerate(zip(wedges, traty_above_5.itertuples())):
    angle = (wedge.theta2 - wedge.theta1) / 2 + wedge.theta1
    x = 1.2 * cos(angle * pi / 180)
    y = 1.2 * sin(angle * pi / 180)
    plt.annotate(f"{row.Категория}: {row.Процент:.1f}%", xy=(x, y), xytext=(1.4 * x, 1.4 * y),
                 ha='center', va='center', fontsize=10, color='black',
                 arrowprops=dict(arrowstyle="-", color='gray'))

st.pyplot(plt)

# Вывод таблицы с форматированием для отображения целых чисел
st.dataframe(traty_above_5.drop(columns=['Процент']).reset_index(drop=True).style.format({'Сумма': '{:.0f}'}).replace(",", " "), use_container_width=True))