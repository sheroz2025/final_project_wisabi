import json
import pandas as pd
import duckdb

DB_FILE = 'my.db'
MAX_ROWS = 1000  # Максимум строк из каждой таблицы

def create_tables():
    try:
        with open('queries/tables.sql') as f:
            sql = f.read()
        with duckdb.connect(DB_FILE) as duck:
            duck.execute(sql)
        print("таблицы созданы успешно.")
    except Exception as e:
        print(f"ошибка при создании таблиц: {e}")


def read_csv(file_name, columns_dict, region=None):
    df = pd.read_csv(f"source/{file_name}.csv", usecols=columns_dict.keys(), nrows=MAX_ROWS)
    df = df.rename(columns=columns_dict)

    date_columns = ["birth_date", "date", "end_of_week"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", format="%m/%d/%Y")

    time_columns = ["start_time", "end_time"]
    for col in time_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", format="%m/%d/%Y %H:%M")

    if region:
        df["region"] = region

    return df


def insert_to_db(df, table_name):
    with duckdb.connect(DB_FILE) as duck:
        duck.execute(f"insert into {table_name} select * from df")
    print(f"загружено {len(df)} строк в {table_name}")


def load_all():
    with open('tables.json') as f:
        tables = json.load(f)

    # сначала не-транзакционные таблицы
    for sheet, props in tables.items():
        table_name = props['table_name']
        columns = props['columns']
        if table_name != 'transactions':
            try:
                file_name = sheet.lower().replace(" ", "_").replace("_lookup", "")
                df = read_csv(file_name, columns)
                insert_to_db(df, table_name)
                print(f"{sheet} → {table_name}")
            except Exception as e:
                print(f"ошибка при загрузке {sheet} → {table_name}: {e}")

    # подготовка данных для фильтрации транзакций
    try:
        with duckdb.connect(DB_FILE) as con:
            valid_cardholders = con.execute("select cardholder_id from customers").fetchdf()
            valid_locations = con.execute("select location_id from atm_location").fetchdf()
            valid_types = con.execute("select transaction_type_id from transaction_type").fetchdf()

        transactions = []
        for sheet, props in tables.items():
            if props['table_name'] == 'transactions':
                file_name = f"{sheet.lower()}_transactions"
                region = sheet.capitalize()
                try:
                    df = read_csv(file_name, props['columns'], region)
                    df = df[df['cardholder_id'].isin(valid_cardholders['cardholder_id'])]
                    df = df[df['location_id'].isin(valid_locations['location_id'])]
                    df = df[df['transaction_type_id'].isin(valid_types['transaction_type_id'])]
                    transactions.append(df)
                    print(f"загружено из {region}: {len(df)} строк")
                except Exception as e:
                    print(f"ошибка с файлом {region}: {e}")

        if transactions:
            final_df = pd.concat(transactions).head(MAX_ROWS * 5)
            with duckdb.connect(DB_FILE) as con:
                con.register("df", final_df)
                con.execute("insert into transactions select * from df")
            print(f"загружено: {len(final_df)} строк в transactions")
        else:
            print("нет данных для загрузки транзакций.")

    except Exception as e:
        print(f"ошибка при загрузке транзакций: {e}")


def create_views():
    try:
        with open('queries/views.sql') as f:
            sql = f.read()
        with duckdb.connect(DB_FILE) as duck:
            duck.execute(sql)
        print("представления созданы успешно.")
    except Exception as e:
        print(f"ошибка при создании представлений: {e}")


def create_n_insert():
    try:
        with duckdb.connect(DB_FILE) as duck:
            duck.execute("select 1 from transactions").fetchone()
        print("база уже инициализирована.")
    except:
        print("инициализация базы данных...")
        create_tables()
        load_all()
        create_views()
        with duckdb.connect(DB_FILE) as duck:
            for tbl in ['transactions', 'customers', 'calendar', 'atm_location']:
                try:
                    count = duck.execute(f"select count(*) from {tbl}").fetchone()[0]
                    print(f"{tbl}: {count} строк")
                except Exception as e:
                    print(f"не удалось прочитать {tbl}: {e}")


if __name__ == "__main__":
    create_n_insert()
