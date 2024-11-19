import psycopg2
import os

def loadEnvFile(filepath):
    with open(filepath, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

loadEnvFile('.env')

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    sslmode=os.getenv("DB_SSLMODE")
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM STORED_URLS;")
rows = cursor.fetchall()

print("Current data in STORED_URLS:")
for row in rows:
    print(row)

cursor.close()
conn.close()
