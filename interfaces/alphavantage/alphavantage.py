import os

import requests

response = requests.get('https://www.alphavantage.co/query', params={
	'function': 'TIME_SERIES_DAILY_ADJUSTED',
	'symbol': 'MSFT',
	'outputsize': 'full',
	'apikey': os.environ['ALPHAVANTAGE_API_KEY'],
}).json()
