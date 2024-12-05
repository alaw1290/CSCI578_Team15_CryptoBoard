import os
import csv
from datetime import date
import hashlib


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

API_KEY = os.getenv('COINMARKETAPI_KEY', '')

"""
{'id': 1, 'name': 'Bitcoin', 'symbol': 'BTC', 'slug': 'bitcoin', 'is_active': 1, 'status': 1, 'first_historical_data': '2010-07-13T00:05:00.000Z', 'last_historical_data': '2024-11-20T04:00:00.000Z', 'platform': None}
{'id': 74, 'name': 'Dogecoin', 'symbol': 'DOGE', 'slug': 'dogecoin', 'is_active': 1, 'status': 1, 'first_historical_data': '2013-12-15T14:40:00.000Z', 'last_historical_data': '2024-11-20T04:00:00.000Z', 'platform': None}
{'id': 825, 'rank': 3, 'name': 'Tether USDt', 'symbol': 'USDT', 'slug': 'tether', 'is_active': 1, 'status': 1, 'first_historical_data': '2015-02-25T13:30:00.000Z', 'last_historical_data': '2024-11-20T04:00:00.000Z', 'platform': {'id': 1, 'name': 'Ethereum', 'symbol': 'ETH', 'slug': 'ethereum', 'token_address': '0xdac17f958d2ee523a2206206994597c13d831ec7'}}
{'id': 1027, 'rank': 2, 'name': 'Ethereum', 'symbol': 'ETH', 'slug': 'ethereum', 'is_active': 1, 'status': 1, 'first_historical_data': '2015-08-07T14:45:00.000Z', 'last_historical_data': '2024-11-20T04:00:00.000Z', 'platform': None}
{'id': 5426, 'rank': 4, 'name': 'Solana', 'symbol': 'SOL', 'slug': 'solana', 'is_active': 1, 'status': 1, 'first_historical_data': '2020-04-10T04:55:00.000Z', 'last_historical_data': '2024-11-20T04:00:00.000Z', 'platform': None}
"""
coinid_map = {
	'1': {'name': 'Bitcoin', 'symbol': 'BTC', 'slug': 'bitcoin', 'max_supply': '21000000', 'infinite_supply': 'False'},
	'74': {'name': 'Dogecoin', 'symbol': 'DOGE', 'slug': 'dogecoin', 'max_supply': '-1', 'infinite_supply': 'True'},
	'825': {'name': 'Tether', 'symbol': 'USDT', 'slug': 'tether',  'max_supply': '-1', 'infinite_supply': 'True'},
	'1027': {'name': 'Ethereum', 'symbol': 'ETH', 'slug': 'ethereum', 'max_supply': '-1', 'infinite_supply': 'True'},
	'5426': {'name': 'Solana', 'symbol': 'SOL', 'slug': 'solana', 'max_supply': '-1', 'infinite_supply': 'True'}
}

def pull_historical_data(id: int, count = 1):
	"""
	Returns a JSON representing latest coinmarket api quote data from quote endpoint on the specified ID value. 
	JSON is structured with the following keys:
	{
		"data": {
			"name": ..., 
			"symbol": ..., 
			"slug": ..., 
			"max_supply": ..., 
			"circulating_supply": ..., 
			"total_supply": ..., 
			"infinite_supply": ..., 
			"cmc_rank": ..., 
			"USD_quote": ..., 
			"USD_market_cap": ..., 
			"last_updated": ...
		}
	}
	"""
	url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/historical'
	parameters = {
		'id':f'{str(id)}',
		'interval': '1h',
		'count': f'{str(count)}'

	}
	headers = {
		'Accepts': 'application/json',
		'X-CMC_PRO_API_KEY': API_KEY,
	}
	session = Session()
	session.headers.update(headers)

	try:
		response = session.get(url, params=parameters)
	except (ConnectionError, Timeout, TooManyRedirects) as e:
		print(e)
		raise e
	info = coinid_map[str(id)]
	response_json = json.loads(response.text)['data']['quotes']

	data = []
	for quote in response_json:
		data.append({
			"coinmarket_id": str(id),
			"name": info['name'], 
			"symbol": info['symbol'], 
			"slug": info['slug'], 
			"max_supply": info['max_supply'], 
			"infinite_supply": info['infinite_supply'],
			"price": quote['quote']['USD']['price'],
			"market_cap": quote['quote']['USD']['market_cap'],
			"total_supply": quote['quote']['USD']['total_supply'], 
			"volume_24h": quote['quote']['USD']['volume_24h'], 
			"percent_change_1h": quote['quote']['USD']['percent_change_1h'], 
			"percent_change_24h": quote['quote']['USD']['percent_change_24h'], 
			"percent_change_7d": quote['quote']['USD']['percent_change_7d'], 
			"percent_change_30d": quote['quote']['USD']['percent_change_30d'], 
			"circulating_supply": quote['quote']['USD']['circulating_supply'],
			"timestamp": quote['quote']['USD']['timestamp']
		})

	return data

def write_out_csv():
	all_data = []
	for id_val in [1, 74, 825, 1027, 5426]:
		all_data += pull_historical_data(id_val, count=504)
	with open('coinmarket_data.csv', 'w') as file:
		datawriter = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		datawriter.writerow(['coinmarket_id', 'name', 'symbol', 'slug', 'max_supply', 'infinite_supply', 'price', 'market_cap', 'total_supply', 'volume_24h', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'percent_change_30d', 'circulating_supply', 'timestamp'])
		for row in all_data:
			datawriter.writerow([row['coinmarket_id'], row['name'], row['symbol'], row['slug'], row['max_supply'], row['infinite_supply'], row['price'], row['market_cap'], row['total_supply'], row['volume_24h'], row['percent_change_1h'], row['percent_change_24h'], row['percent_change_7d'], row['percent_change_30d'], row['circulating_supply'], row['timestamp']])

if __name__ == '__main__':
	write_out_csv()

