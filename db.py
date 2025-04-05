import duckdb
import pandas as pd

DB_FILE = 'my.db'

# ------------------------- Универсальный SQL-загрузчик -------------------------
def load_sql_query(query: str) -> pd.DataFrame:
    with duckdb.connect(DB_FILE) as duck:
        return duck.query(query).to_df()

# ------------------------- Дата границы транзакций -------------------------
def fetch_date_boundaries():
    with duckdb.connect(DB_FILE) as duck:
        min_date, max_date = duck.query("""
            select
                min(start_time) as min_date,
                max(start_time) as max_date
            from transactions
        """).fetchone()
        return min_date, max_date

# ------------------------- Загрузка клиентов с возрастом и стажем -------------------------
def fetch_customers(report_date):
    query = f"""
        select *
        from v_customers_with_age_duration
    """
    return load_sql_query(query)

# ------------------------- Все транзакции из представления -------------------------
def fetch_all_transactions():
    return load_sql_query("select * from v_transactions")

# ------------------------- Фильтрованные транзакции -------------------------
def fetch_filtered_transactions(start_date=None, end_date=None, region=None, gender=None):
    query = "select * from v_transactions where 1=1"
    if start_date:
        query += f" and start_time >= cast('{start_date}' as date)"
    if end_date:
        query += f" and start_time <= cast('{end_date}' as date)"
    if region:
        query += f" and region = '{region}'"
    if gender:
        query += f" and gender = '{gender}'"
    return load_sql_query(query)

# ------------------------- Кол-во транзакций по полу -------------------------
def fetch_transaction_counts_by_gender():
    return load_sql_query("""
        select gender, transaction_count
        from v_transaction_count_gender
    """)

# ------------------------- Топ-10 клиентов -------------------------
def fetch_top_clients():
    return load_sql_query("select * from v_top_clients")

# ------------------------- Сумма транзакций по регионам -------------------------
def fetch_transaction_amount_by_region():
    return load_sql_query("select * from v_transaction_amount_region")

# ------------------------- Сумма транзакций по типам счетов -------------------------
def fetch_transaction_amount_by_account_type():
    return load_sql_query("select * from v_transaction_amount_by_account_type")

# ------------------------- Средняя сумма транзакции по профессиям -------------------------
def fetch_avg_transaction_by_occupation():
    return load_sql_query("select * from v_avg_transaction_by_occupation")

# ------------------------- Транзакции по дням недели -------------------------
def fetch_transaction_by_weekday():
    return load_sql_query("select * from v_transaction_by_weekday")

# ------------------------- Транзакции по часам -------------------------
def fetch_transaction_by_hour():
    return load_sql_query("select * from v_transaction_by_hour")

# ------------------------- Распределение по возрасту -------------------------
def fetch_transaction_by_age():
    return load_sql_query("select * from v_transaction_age_group")