import psycopg2
import os

# Load environment variables
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
cursor.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = 'stored_urls';
""")

columns = cursor.fetchall()
print("Table structure for STORED_URLS:")
for column in columns:
    print(column)

cursor.close()
conn.close()
