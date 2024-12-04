import requests

BASE_URL = "http://127.0.0.1:8000/crawl"

cryptos = ["Tether", "Ethereum", "Solana", "Dogecoin", "Bitcoin"]
sources = ["cnn.com", "foxnews.com", "reddit.com"]
number_of_results = 100

for crypto in cryptos:
    for source in sources:
        print(f"Fetching {number_of_results} links for {crypto} from {source}...")
        response = requests.get(
            BASE_URL,
            params={"sourceName": source, "cryptoName": crypto, "number": number_of_results}
        )
        if response.status_code == 200:
            print(f"Successfully fetched links for {crypto} from {source}")
        else:
            print(f"Failed to fetch links for {crypto} from {source}: {response.text}")