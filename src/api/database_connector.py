import psycopg2
from db_conn_config import DATABASE_CONFIG
import pandas as pd

def connect_to_db():
    """
    Connect to the existing PostgreSQL database.
    """
    return psycopg2.connect(**DATABASE_CONFIG)

def execute_sql_query(sql_query: str):
    """
    Execute the generated SQL query and return results.
    """
    conn = connect_to_db()
    try:
        # Use pandas to execute the query and fetch results
        df = pd.read_sql(sql_query, conn)
        return df
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()


  