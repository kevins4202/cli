import pyodbc
import json

def check_table_exists(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'")
    return cursor.fetchone()[0] > 0

def create_tables_if_needed(cursor):
    with open('cats.txt', 'r') as f:
        categories = [line.strip() for line in f.readlines()]

    for category in categories:
        table_name = category.lower()
        if not check_table_exists(cursor, table_name):
            cursor.execute(f"""
                CREATE TABLE {table_name} (
                    id INT PRIMARY KEY IDENTITY(1,1),
                    headline NVARCHAR(500) NOT NULL,
                    url NVARCHAR(2000) NOT NULL,
                    created_at DATETIME2 DEFAULT GETUTCDATE()
                )
            """)

def insert_news_data(cursor, category, news_list):
    table_name = category.lower()
    for news in news_list:
        cursor.execute(f"""
            INSERT INTO {table_name} (headline, url)
            VALUES (?, ?)
        """, (news['headline'], news['url']))

def connect_to_azure_sql(server, database, username, password):
    conn_str = (
        r"DRIVER={ODBC Driver 17 for SQL Server};"
        r"SERVER=" + server + ";"
        r"DATABASE=" + database + ";"
        r"Trusted_Connection=no;"
        r"UID=" + username + ";"
        r"PWD=" + password + ";"
    )

    try:
        conn = pyodbc.connect(conn_str)
        print("Connected to Azure SQL Database")
        return conn
    except pyodbc.Error as e:
        print("Error connecting to database:", e)
        return None

def main():
    server = 'your_server_name.database.windows.net'
    database = 'your_database_name'
    username = 'your_username'
    password = 'your_password'

    conn = connect_to_azure_sql(server, database, username, password)
    if conn:
        cursor = conn.cursor()

        create_tables_if_needed(cursor)

        with open('result.json', 'r') as f:
            data = json.load(f)

        for category, news_list in data.items():
            insert_news_data(cursor, category, news_list)

        conn.commit()
        conn.close()

if __name__ == "__main__":
    main()