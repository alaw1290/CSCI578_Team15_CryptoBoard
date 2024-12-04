import os
import time
import praw
import csv
from dotenv import load_dotenv
from datetime import datetime


# Load environment variables from .env file
def load_env_file(filepath):
    load_dotenv(filepath)


def format_timestamp(unix_timestamp):
    dt = datetime.utcfromtimestamp(unix_timestamp)  # Convert to UTC datetime
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f")


# Initialize Reddit API client
def initialize_reddit():
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
        user_agent="Cryptoboard (by u/sosollasi)"
    )


# Fetch posts for a cryptocurrency
def fetch_posts(reddit, crypto_name):
    subreddit = reddit.subreddit("CryptoCurrency")
    posts = []
    for post in subreddit.search(crypto_name, sort="new", limit=100):
        # Extract post details
        posts.append({
            "crypto_name": crypto_name,
            "source": "reddit.com",
            "url": post.url,
            "id": post.id,
            "title": post.title,
            "published_date": format_timestamp(post.created_utc),  # Timestamp (in seconds since epoch)
            "summary": post.selftext if post.is_self else post.url,  # Post text or external URL
            "upvotes": post.score,
            "comment_count": post.num_comments
        })
    return posts


# Write data to CSV
def write_to_csv(filename, posts):
    # Check if file exists to decide if headers are needed
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "crypto_name", "source", "url", "id", "title", "published_date", "summary", "upvotes", "comment_count"
        ])
        if not file_exists:
            writer.writeheader()  # Write headers if the file is new
        writer.writerows(posts)  # Append rows


# Main script
if __name__ == "__main__":
    # Load environment variables
    load_env_file('../.env')

    # Initialize Reddit client
    reddit = initialize_reddit()

    # List of cryptocurrencies
    cryptos = ["Bitcoin", "Tether", "Ethereum", "Solana", "Dogecoin"]

    # Output CSV file
    output_csv = "reddit_posts.csv"

    # Fetch and store posts
    for crypto in cryptos:
        print(f"Fetching posts for {crypto}...")
        posts = fetch_posts(reddit, crypto)
        print(f"Fetched {len(posts)} posts for {crypto}. Writing to CSV...")
        write_to_csv(output_csv, posts)
        print(f"Stored posts for {crypto} in {output_csv}.")

    print("Done!")
