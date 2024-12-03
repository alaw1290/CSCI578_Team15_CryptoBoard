import re
from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import requests, os, psycopg2
import nltk, time, random
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from db_connector import create_connection


# Need to download pre-trained models the first time you run this
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')

app = Flask(__name__, template_folder='templates')
executor = ThreadPoolExecutor(max_workers=5)

app.logger.debug('Running cryptoboard')

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

def getSentimentOutput(summary):

    # Tokenize the text
    tokens = word_tokenize(summary.lower())
    # Remove stop words
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    # Join the tokens back into a string
    processed_text = ' '.join(lemmatized_tokens)
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(processed_text)
    # Sentiment is 1 if more positive, -1 if more negative, else 0
    if scores['pos'] > scores['neg']:
        sentiment = 1
    elif scores['pos'] < scores['neg']:
        sentiment = -1
    else:
        sentiment = 0
    return sentiment

# runs query against database
def query_database(query):
    records = None
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        connection.close()
        return records


# get all available cryptos 
@app.route("/available_cryptos", methods=['GET'])
def all_cryptos():
    records = query_database(f"SELECT * FROM coinmarket_id_map")
    results = []
    if records:
        for record in records:
            results.append({
                'coinmarket_id': record[0],
                'crypto_name': record[1],
                'crypto_symbol': record[2]
            })

    return jsonify(results)


@app.route("/<crypto_id>/data", methods=['GET'])
def get_crypto_data(crypto_id):
    
    crypto_id = re.sub(r'\W+', '', crypto_id)

    records = query_database(f"SELECT * FROM coinmarket_data WHERE coinmarket_id = {crypto_id}")

    results = []
    for record in records:
        results.append({
            'id': record[0],
            'coinmarket_id': record[1],
            'name': record[2],
            'symbol': record[3],
            'slug': record[4],
            'max_supply': record[5],
            'circulating_supply': record[6],
            'total_supply': record[7],
            'infinite_supply': record[8],
            'cmc_rank': record[9],
            'USD_quote': record[10],
            'USD_market_cap': record[11],
            'last_updated': record[12]
        })

    return jsonify(results)


@app.route("/<crypto_id>/articles", methods=['GET'])
def get_crypto_articles(crypto_id):
    
    crypto_id = re.sub(r'\W+', '', crypto_id)

    records = query_database(f"SELECT name FROM coinmarket_id_map WHERE coinmarket_id = {crypto_id}")

    crypto_name = records[0][0].strip()
    records = query_database(f"SELECT U.*, S.sentiment FROM stored_urls U INNER JOIN stored_urls_sentiment S on U.id = S.id WHERE crypto_name = '{crypto_name}'")


    results = []
    for record in records:
        results.append({
            'crypto_name': record[0],
            'source': record[1],
            'url': record[2],
            'id': record[3],
            'title': record[4],
            'published_date': record[5],
            'summary': record[6],
            'sentiment': record[7]
        })

    return jsonify(results)



@app.route("/sentiment", methods=['POST'])
def calculate_sentiment():
    request_data = request.get_json()
    text = request_data.get('text')
    results = getSentimentOutput(text)
    return jsonify(results)


@app.route("/", methods=['GET'])
def hello_world(name='User'):
    return render_template('hello.html', person=name)


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