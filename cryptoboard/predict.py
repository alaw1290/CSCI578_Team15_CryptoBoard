import psycopg2
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime
from dotenv import load_dotenv
import os

def load_from_database():
    # Load environment variables from .env file
    load_dotenv()

    # Database connection parameters from environment variables
    DB_NAME = os.getenv('POSTGRES_DB_NAME')
    DB_USER = os.getenv('POSTGRES_USER')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    DB_HOST = os.getenv('POSTGRES_DB_HOST')
    DB_PORT = os.getenv('POSTGRES_DB_PORT', 5432)  # Default PostgreSQL port

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    # Query to retrieve data
    query = """
    SELECT data_timestamp as timestamp, price
    FROM coinmarket_data
    ORDER BY data_timestamp desc
    """

    # Load data into a pandas DataFrame
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()
    return df

def load_from_file():
    # Load data from the local CSV file
    file_path = '../dataset/coinmarket_data.csv'
    # Convert the file path to an absolute path
    file_path = os.path.abspath(file_path)
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()  
    return df

def get_symbols(df):
    # Get list of unique values in the symbol column and strip spaces
    unique_symbols = [symbol.strip() for symbol in df['symbol'].unique()]
    print(unique_symbols)
    return unique_symbols


def predict_price(df, symbol):
    # List all the columns in the DataFrame
    print(df.columns)

    # Filter the DataFrame for the specific symbol
    df = df[df['symbol'].str.strip() == symbol].copy()

    # Check if required columns exist
    if 'timestamp' not in df.columns or 'price' not in df.columns:
        raise KeyError("The required columns 'timestamp' or 'price' are not present in the data.")

    # Convert last_updated to datetime and extract features
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['timestamp'] = df['timestamp'].apply(lambda x: x.timestamp())
    
    # Prepare the data for the model
    X = df[['timestamp']]
    y = df['price']

    # Train a simple linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict future prices
    future_dates = pd.date_range(start=df['timestamp'].max(), periods=30, freq='D')
    future_timestamps = pd.DataFrame(future_dates.map(lambda x: x.timestamp()), columns=['timestamp'])
    predictions = model.predict(future_timestamps)

    # Output predictions
    print(symbol)
    for date, price in zip(future_dates, predictions):
        print(f"Date: {date.date()}, Predicted Price: ${price:.2f}")


def main():
    # Load data from the database
    df = load_from_file()

    # Get list of unique symbols
    symbols = get_symbols(df)

    # Predict future prices for each symbol
    for symbol in symbols:
        print(f"Predicting prices for {symbol}")
        predict_price(df, symbol)

if __name__ == '__main__':
    main()