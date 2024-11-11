from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def googleSearch(sourceName, cryptoName, numberOfResultsToCrawl):
    try:
        query = f"site:{sourceName} {cryptoName}"
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num={numberOfResultsToCrawl}"
        print(search_url)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(search_url, headers=headers, verify=False)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, "html.parser")
        uniqueLinks = set() 
        links = []
        
        for item in soup.find_all('a', href=True):
            print('\n' + str(item) + '\n')
            href = item['href']
            if href.startswith("https://")  and "google.com" not in href and "/search" not in href:
                if href not in uniqueLinks:
                    uniqueLinks.add(href)
                    links.append(href)
                if len(links) >= numberOfResultsToCrawl:
                    break
        return links[:numberOfResultsToCrawl]
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return {"error": "Failed fetching results from Google"}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Unexpected error in google search scope"}
    
@app.route('/crawl', methods=['GET'])
def crawl():
    try:
        sourceName = request.args.get('sourceName')
        cryptoName = request.args.get('cryptoName')
        numberOfResultsToCrawl = request.args.get('number', 10, type=int)
        results = googleSearch(sourceName, cryptoName, numberOfResultsToCrawl)
        return jsonify({
                "sourceName": sourceName,
                "cryptoName": cryptoName,
                "links": results
        })
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Unexpected error in crawling scope"}

if __name__ == '__main__':
    app.run(port=8000, debug=True)
    # Example request:
    # http://127.0.0.1:8000/crawl?sourceName=nytimes.com&cryptoName=Bitcoin&number=30