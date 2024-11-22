import os
import psycopg2

# Connector setup
conn = psycopg2.connect(
    host=os.environ['POSTGRES_DB_HOST'],
    database=os.environ['POSTGRES_DB_NAME'],
    user=os.environ['POSTGRES_DB_USERNAME'],
    password=os.environ['POSTGRES_DB_PASSWORD']
)

# Open a cursor to perform database operations
cur = conn.cursor()

cur.close()
conn.close()

print('finished')