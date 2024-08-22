# connection.py

import psycopg2

def get_db_connection():
    """
    Establishes and returns a connection to the PostgreSQL database.
    Make sure to replace the connection details with your actual database configuration.
    """
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Odoo17",
            user="odoo",
            password="shashi"
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise
