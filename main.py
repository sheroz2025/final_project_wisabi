import streamlit as st
import pandas as pd
import plotly.express as px
import db

# Настройки страницы
st.set_page_config(page_title="Дашборд Wisabi Bank", layout="wide")

# Боковая панель навигации
st.sidebar.title("Навигация")
selected_tab = st.sidebar.radio("Выберите раздел:", ["Общие показатели", "Поведение клиентов", "По полу"])

# Загружаем данные
transactions = db.fetch_all_transactions()
top_clients = db.fetch_top_clients()
by_region = db.fetch_transaction_amount_by_region()
by_account = db.fetch_transaction_amount_by_account_type()
avg_by_occupation = db.fetch_avg_transaction_by_occupation()
by_gender = db.fetch_transaction_counts_by_gender()
by_weekday = db.fetch_transaction_by_weekday()
by_hour = db.fetch_transaction_by_hour()
by_age = db.fetch_transaction_by_age()

st.title("Дашборд: Клиенты и транзакции Wisabi Bank")

if selected_tab == "Общие показатели":
    # Метрики
    col1, col2, col3 = st.columns(3)
    col1.metric("Всего транзакций", len(transactions))
    col2.metric("Сумма транзакций", f"{transactions['amount'].sum():,.0f}")
    col3.metric("Число клиентов", transactions['cardholder_id'].nunique())

    st.subheader("Сумма по регионам")
    st.plotly_chart(px.pie(by_region, names="region", values="total_amount", title="Сумма транзакций по регионам"))

    st.subheader("Счета")
    st.plotly_chart(px.bar(by_account, x="account_type", y="total_amount", title="Транзакции по типам счетов"))

    st.subheader("Средняя сумма по профессиям")
    st.plotly_chart(px.bar(avg_by_occupation, x="occupation", y="avg_transaction", title="Средняя сумма по профессиям"))

    st.subheader("Топ-10 клиентов")
    st.plotly_chart(px.bar(top_clients, x="full_name", y="total_amount", title="Топ-10 клиентов по сумме транзакций"))

elif selected_tab == "Поведение клиентов":
    st.subheader("Транзакции по дням недели")
    st.plotly_chart(px.bar(by_weekday, x="day_name", y="transaction_count", title="Транзакции по дням недели"))

    st.subheader("Транзакции по часам")
    st.plotly_chart(px.line(by_hour, x="hour", y="transaction_count", title="Активность по часам", markers=True))

    st.subheader("Распределение суммы по возрасту")
    st.plotly_chart(px.area(by_age, x="age", y="total_amount", title="Сумма по возрасту"))

elif selected_tab == "По полу":
    st.subheader("Распределение транзакций по полу")
    st.plotly_chart(px.pie(by_gender, names="gender", values="transaction_count", title="Транзакции по полу"))


