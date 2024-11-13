import os
import pyodbc

# Retrieve the connection string from the environment variable
connection_string = os.getenv("AZURE_SQL_CONNECTION_STRING")

# Check if the connection string is set
if connection_string:
    try:
        # Connect to the Azure SQL Database
        conn = pyodbc.connect(connection_string)
        print("Connected to the database successfully!")

        # Example query
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 10 * FROM your_table_name")
        for row in cursor.fetchall():
            print(row)

        # Close connection
        conn.close()
    except Exception as e:
        print("Failed to connect to the database")
        print(e)
else:
    print("Connection string not found. Please set the AZURE_SQL_CONNECTION_STRING environment variable.")
