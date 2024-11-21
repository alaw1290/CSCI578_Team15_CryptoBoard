import psycopg2
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random
import time
from dateutil import parser


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
cursor = conn.cursor()


def extract_summary_from_meta(soup):
    """Extract summary from various metadata tags."""
    meta_tags = [
        {"name": "description"},  # Common description tag
        {"property": "og:description"},  # OpenGraph description
        {"property": "twitter:description"},  # Twitter card description
        {"name": "summary"},  # Less common but possible
    ]
    for tag in meta_tags:
        meta = soup.find("meta", tag)
        if meta and meta.get("content"):
            return meta.get("content").strip()
    return None


def extract_summary_from_paragraphs(soup):
    """Extract the first meaningful paragraph as a summary."""
    for paragraph in soup.find_all("p"):
        text = paragraph.get_text(strip=True)
        if text:  # Check if the paragraph is not empty
            return text
    return None


def extract_summary_with_headings(soup):
    """Combine the main heading and first paragraph for a fallback summary."""
    heading = soup.find("h1").get_text(strip=True) if soup.find("h1") else None
    first_paragraph = extract_summary_from_paragraphs(soup)
    if heading and first_paragraph:
        return f"{heading} - {first_paragraph}"
    return heading or first_paragraph


def extract_published_date(soup):
    """Attempts to extract published date from various meta tags."""
    possible_tags = [
        "article:published_time", "og:published_time",
        "datePublished", "publish_date", "pub_date", "date"
    ]
    for meta in soup.find_all("meta"):
        if meta.get("property") in possible_tags or meta.get("name") in possible_tags:
            date_str = meta.get("content")
            if date_str:
                try:
                    return parser.parse(date_str)
                except ValueError:
                    continue
    return None


def extract_summary(soup):
    summary = extract_summary_from_meta(soup)
    if summary:
        print("Summary extracted from metadata.")
        return summary

    summary = extract_summary_from_paragraphs(soup)
    if summary:
        print("Summary extracted from the first paragraph.")
        return summary

    summary = extract_summary_with_headings(soup)
    if summary:
        print("Summary extracted using headings.")
        return summary

    print("No summary found.")
    return "Summary not available."


def fetch_url_details(url):
    """Retrieve title, published date, and summary from an HTML page."""
    try:
        # Random sleep to avoid detection as a bot
        sleep_time = random.uniform(1, 10)
        print(f"Sleeping for {sleep_time:.2f} seconds before requesting {url}")
        time.sleep(sleep_time)

        # Request the page
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
        response.raise_for_status()

        # Check if the content type is HTML
        if "text/html" not in response.headers["Content-Type"]:
            print(f"Skipping non-HTML URL: {url}")
            return None, None, None  # Skip non-HTML content

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the title
        title = soup.title.string.strip() if soup.title else None

        # Extract the published date using the previously added robust function
        published_date = extract_published_date(soup)

        # Extract the summary using the combined strategy
        summary = extract_summary(soup)

        return title, published_date, summary

    except requests.RequestException as e:
        print(f"Request error for URL {url}: {e}")
        return None, None, None


# def fetch_url_details(url):
#     """Retrieve title, published date, and summary from an HTML page."""
#     try:
#         # Request the page
#         response = requests.get(url, headers={
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#         })
#         response.raise_for_status()
#
#         # Check if the content type is HTML
#         if "text/html" not in response.headers["Content-Type"]:
#             print(f"Skipping non-HTML URL: {url}")
#             return None, None, None  # Skip non-HTML content
#
#         soup = BeautifulSoup(response.text, "html.parser")
#
#         # Extract the title
#         title = soup.title.string if soup.title else None
#
#         # Extract the published date from meta tags (if available)
#         published_date = None
#         for meta in soup.find_all("meta"):
#             if meta.get("property") in ["article:published_time", "og:published_time"]:
#                 published_date = meta.get("content")
#                 break
#         if published_date:
#             try:
#                 published_date = datetime.fromisoformat(published_date)
#             except ValueError:
#                 published_date = None
#
#         # Extract summary based on the "summary:" keyword
#         summary = None
#         for p in soup.find_all("p"):
#             if "summary:" in p.get_text().lower():
#                 summary = p.get_text().split("summary:", 1)[1].strip()
#                 break
#
#         return title, published_date, summary
#
#     except requests.RequestException as e:
#         print(f"Request error for URL {url}: {e}")
#         return None, None, None


def update_url_info():
    """Fetch URLs from the database, retrieve HTML content info, and update the database."""
    # Fetch URLs that need information (e.g., where title is NULL)
    cursor.execute("SELECT id, url FROM STORED_URLS WHERE published_date IS NULL;")
    urls = cursor.fetchall()

    for url_id, url in urls:
        title, published_date, summary = fetch_url_details(url)

        # If we retrieved any data, update the database
        if title or published_date or summary:
            cursor.execute("""
                UPDATE STORED_URLS
                SET title = %s, published_date = %s, summary = %s
                WHERE id = %s;
            """, (title, published_date, summary, url_id))
            conn.commit()
            print(f"Updated information for URL {url}")


update_url_info()

# Close the cursor and the database connection
cursor.close()
conn.close()
