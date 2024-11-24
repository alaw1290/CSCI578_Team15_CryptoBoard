import os
from datetime import date
import hashlib


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

API_KEY = os.getenv('COINMARKETAPI_KEY', '')

"""
{'id': 1, 'rank': 1, 'name': 'Bitcoin', 'symbol': 'BTC', 'slug': 'bitcoin', 'is_active': 1, 'status': 1, 'first_historical_data': '2010-07-13T00:05:00.000Z', 'last_historical_data': '2024-11-20T04:00:00.000Z', 'platform': None}
{'id': 74, 'rank': 7, 'name': 'Dogecoin', 'symbol': 'DOGE', 'slug': 'dogecoin', 'is_active': 1, 'status': 1, 'first_historical_data': '2013-12-15T14:40:00.000Z', 'last_historical_data': '2024-11-20T04:00:00.000Z', 'platform': None}
{'id': 825, 'rank': 3, 'name': 'Tether USDt', 'symbol': 'USDT', 'slug': 'tether', 'is_active': 1, 'status': 1, 'first_historical_data': '2015-02-25T13:30:00.000Z', 'last_historical_data': '2024-11-20T04:00:00.000Z', 'platform': {'id': 1, 'name': 'Ethereum', 'symbol': 'ETH', 'slug': 'ethereum', 'token_address': '0xdac17f958d2ee523a2206206994597c13d831ec7'}}
{'id': 1027, 'rank': 2, 'name': 'Ethereum', 'symbol': 'ETH', 'slug': 'ethereum', 'is_active': 1, 'status': 1, 'first_historical_data': '2015-08-07T14:45:00.000Z', 'last_historical_data': '2024-11-20T04:00:00.000Z', 'platform': None}
{'id': 5426, 'rank': 4, 'name': 'Solana', 'symbol': 'SOL', 'slug': 'solana', 'is_active': 1, 'status': 1, 'first_historical_data': '2020-04-10T04:55:00.000Z', 'last_historical_data': '2024-11-20T04:00:00.000Z', 'platform': None}
"""

def pull_latest_quote_data(id: int):
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
	url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
	parameters = {
		'id':f'{str(id)}',
		'aux': 'cmc_rank,max_supply,circulating_supply,total_supply'
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
		raise 

	response_json = json.loads(response.text)['data'][str(id)]


	data = {
		"data": {
			"name": response_json['name'], 
			"symbol": response_json['symbol'], 
			"slug": response_json['slug'], 
			"max_supply": -1 if response_json['max_supply'] is None else response_json['max_supply'], 
			"circulating_supply": response_json['circulating_supply'], 
			"total_supply": response_json['total_supply'], 
			"infinite_supply": response_json['infinite_supply'], 
			"cmc_rank": response_json["cmc_rank"], 
			"USD_quote": response_json['quote']['USD']['price'], 
			"USD_market_cap": response_json['quote']['USD']['market_cap'], 
			"last_updated": response_json['last_updated']
		}
	}
	# data = {'data': {'name': 'Bitcoin', 'symbol': 'BTC', 'slug': 'bitcoin', 'max_supply': 21000000, 'circulating_supply': 19786525, 'total_supply': 19786525, 'infinite_supply': False, 'cmc_rank': 1, 'USD_quote': 98375.43008370513, 'USD_market_cap': 1946507906736.9836, 'last_updated': '2024-11-24T02:06:00.000Z'}}
	return data


if __name__ == '__main__':
	print(pull_latest_quote_data(74))

