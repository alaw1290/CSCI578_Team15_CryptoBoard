from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import requests, os, psycopg2
import time
import random

from db_connector import create_connection

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=5)

def loadEnvFile(filepath):
    with open(filepath, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value


''''def is_html_url(href):
    """Check if the URL is likely an HTML page."""
    return (href.startswith("https://") and
            "google.com" not in href and
            "/search" not in href and
            (href.endswith(".html") or
             href.endswith(".htm") or
             "/article" in href or
             "/news" in href or
             "/story" in href))'''


def googleSearch(sourceName, cryptoName, numberOfResultsToCrawl):
    try:
        '''More than one user agent so the IP does not get blocked by google'''
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        ]
        query = f"site:{sourceName} {cryptoName}"
        headers = {
            "User-Agent": random.choice(user_agents)
        }
        uniqueLinks = set()
        links = []
        
        loadEnvFile('../.env')
    
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            sslmode=os.getenv("DB_SSLMODE"),
            sslrootcert=os.getenv("DB_SSLROOTCERT")
        )
        
        cursor = conn.cursor()
        
        for start in range(0, numberOfResultsToCrawl, 10):  # Adjust increment to match Google results per page
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num=10&start={start}"
            print(f"Fetching results from: {search_url}")

            response = requests.get(search_url, headers=headers, verify=False)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            for item in soup.find_all('a', href=True):
                href = item['href']
                # HTML filtering criteria
                if href.startswith("https://") and "google.com" not in href and "/search" not in href and (
                        href.endswith(".html") or href.endswith(
                    ".htm") or "/article" in href or "/news" in href or "/story" or "/blog" in href or "/post" in href 
                            or "/topic" in href or "/page" in href or href.split("/")[-1].isdigit()
                ):
                    if href not in uniqueLinks:
                        # Check if URL already exists in the database
                        cursor.execute("SELECT 1 FROM STORED_URLS WHERE URL = %s;", (href,))
                        queryResults = cursor.fetchone()
                        if queryResults is None:
                            uniqueLinks.add(href)
                            links.append(href)
                            try:
                                # Insert into the database
                                cursor.execute(
                                    "INSERT INTO STORED_URLS (CRYPTO_NAME, SOURCE, URL) VALUES (%s, %s, %s);",
                                    (cryptoName, sourceName, href))
                                conn.commit()
                                print(f"{len(links)} - {href} has been stored.")
                            except Exception as e:
                                conn.rollback()
                                print(f"An error occurred: {e}")

                if len(links) >= numberOfResultsToCrawl:
                    break
            
            # replicate human waiting time and prevent from getting blocked
            time.sleep(2)

            if len(links) >= numberOfResultsToCrawl:
                break

        cursor.close()
        conn.close()
        return links[:numberOfResultsToCrawl]
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return {"error": "Failed fetching results from Google"}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Unexpected error in google search scope"}

# Calling googleSearch function by different threads
def asyncGoogleSearch(sourceName, cryptoName, numberOfResultsToCrawl):
    return executor.submit(googleSearch, sourceName, cryptoName, numberOfResultsToCrawl)

@app.route("/", methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/test", methods=['GET'])
def test_db_conn():
    connection = create_connection()
    cursor = connection.cursor()

    # Fetch all rows from database
    cursor.execute("SELECT * from coinmarket_id_map;")
    records = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return str(records)


@app.route('/crawl', methods=['GET'])
def crawl():
    try:
        sourceName = request.args.get('sourceName')
        cryptoName = request.args.get('cryptoName')
        numberOfResultsToCrawl = request.args.get('number', 10, type=int)
        
        #results = googleSearch(sourceName, cryptoName, numberOfResultsToCrawl)
        future = asyncGoogleSearch(sourceName, cryptoName, numberOfResultsToCrawl)
        results = future.result()
        
        return jsonify({
            "sourceName": sourceName,
            "cryptoName": cryptoName,
            "links": results
        })
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Unexpected error in crawling scope"}

if __name__ == '__main__':
    app.run(port=8000, debug=True, threaded=True)
    # Example request:
    # http://127.0.0.1:8000/crawl?sourceName=nytimes.com&cryptoName=Bitcoin&number=30