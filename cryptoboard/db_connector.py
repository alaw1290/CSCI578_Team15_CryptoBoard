import os
import psycopg2

def create_connection():
    """
    Returns a DB connection to the local database. 
    Remember to close connection after use, i.e.
    ```
    cur = conn.cursor()
    ...
    perform ops
    ...
    cur.close()
    conn.close()
    ```
    """
    # Connector setup
    conn = psycopg2.connect(
        host=os.environ['POSTGRES_DB_HOST'],
        port=os.environ['POSTGRES_DB_PORT'],
        database=os.environ['POSTGRES_DB_NAME'],
        user=os.environ['POSTGRES_DB_USERNAME'],
        password=os.environ['POSTGRES_DB_PASSWORD']
    )

    return conn