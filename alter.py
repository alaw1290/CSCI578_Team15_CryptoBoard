import psycopg2
import os

# Function to load environment variables from the .env file
def loadEnvFile(filepath):
    with open(filepath, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Load the .env file with database credentials
loadEnvFile('.env')

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    sslmode=os.getenv("DB_SSLMODE")
)

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# SQL command to alter the STORED_URLS table (adding columns and setting NOT NULL)
alter_table_query = """
    ALTER TABLE STORED_URLS
    ADD COLUMN IF NOT EXISTS id SERIAL PRIMARY KEY,
    ADD COLUMN IF NOT EXISTS title TEXT,
    ADD COLUMN IF NOT EXISTS published_date TIMESTAMP,
    ADD COLUMN IF NOT EXISTS summary TEXT,
    ALTER COLUMN url SET NOT NULL;
"""

try:
    # Execute the ALTER TABLE command to add columns and set NOT NULL
    cursor.execute(alter_table_query)
    conn.commit()  # Commit changes
    print("Columns added and NOT NULL constraint set successfully.")

    # Check if the 'url_unique' constraint already exists
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.table_constraints
        WHERE table_name = 'stored_urls' AND constraint_name = 'url_unique';
    """)
    constraint_exists = cursor.fetchone()[0]

    # Add the 'url_unique' constraint if it doesn't exist
    if constraint_exists == 0:
        cursor.execute("ALTER TABLE STORED_URLS ADD CONSTRAINT url_unique UNIQUE (url);")
        conn.commit()
        print("Unique constraint 'url_unique' added to 'url' column.")
    else:
        print("Unique constraint 'url_unique' already exists.")

except Exception as e:
    # Roll back changes if an error occurs
    conn.rollback()
    print(f"An error occurred: {e}")
finally:
    # Close the cursor and the database connection
    cursor.close()
    conn.close()
