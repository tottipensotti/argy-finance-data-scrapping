import requests
import json
import os
import datetime

url = "https://analisistecnico.com.ar/services/datafeed/history"
cedears_file = os.path.join('..', 'data', 'cedears.json')

# ticker = "AAPL"

start_date = "2024/01/01"
end_date = "2024/08/31"
start_date = datetime.datetime.strptime(start_date, "%Y/%m/%d")
end_date = datetime.datetime.strptime(end_date, "%Y/%m/%d")
_from = int(start_date.timestamp())
_to = int(end_date.timestamp())
raw_data = {}

with open(cedears_file, 'r') as file:
    cedears_dict = json.load(file)
    tickers = cedears_dict.keys()

for ticker in tickers:
    try:
        request_url = f"{url}?symbol={ticker}%3ACEDEAR&resolution=D&from={_from}&to={_to}"
        response = requests.get(request_url)
        raw_data[ticker] = response.json()
        print(f"Request for {ticker} data from {start_date} to {end_date} successfully made.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {ticker}: {e}")
        response.raise_for_status()