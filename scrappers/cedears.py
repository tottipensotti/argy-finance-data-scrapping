import requests
import json
import os
import datetime

url = "https://analisistecnico.com.ar/services/datafeed/history"
cedears_file = os.path.join('..', 'data', 'cedears.json')

start_date = "2024/01/01"
end_date = "2024/09/01"
start_date = datetime.datetime.strptime(start_date, "%Y/%m/%d")
end_date = datetime.datetime.strptime(end_date, "%Y/%m/%d")
date_from = int(start_date.timestamp())
date_to = int(end_date.timestamp())

raw_data = {}
processed_data = {}

with open(cedears_file, 'r') as file:
    cedears_dict = json.load(file)
    tickers_list = cedears_dict.keys()

def extract_data(tickers, url, _from, _to):
    for ticker in list(tickers):
        try:
            request_url = f"{url}?symbol={ticker}%3ACEDEAR&resolution=D&from={_from}&to={_to}"
            response = requests.get(request_url)
            raw_data[ticker] = response.json()
            print(f"Request for {ticker} data from {start_date} to {end_date} successfully made.")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {ticker}: {e}")
            response.raise_for_status()
    return raw_data

def process_data(raw_data):
    for ticker in raw_data.keys():
        if isinstance(raw_data[ticker], dict):
            if 't' not in raw_data[ticker]:
                print(f"Error: 't' key is missing for ticker {ticker}.")
                continue

            timestamps = raw_data[ticker]['t']
            required_keys = ['o', 'h', 'l', 'c', 'v']
            if not all(key in raw_data[ticker] for key in required_keys):
                print(f"Error: One or more required keys are missing for ticker {ticker}.")
                continue
            
            if not all(len(raw_data[ticker][key]) == len(timestamps) for key in required_keys):
                print(f"Error: Data lists for ticker {ticker} are not of the same length.")
                continue
            
            for i, date in enumerate(timestamps):
                formatted_date = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d')
                
                if formatted_date not in processed_data:
                    processed_data[formatted_date] = {}
                    
                processed_data[formatted_date][ticker] = {
                    'open': raw_data[ticker]['o'][i],
                    'high': raw_data[ticker]['h'][i],
                    'low': raw_data[ticker]['l'][i],
                    'close': raw_data[ticker]['c'][i],
                    'volume': raw_data[ticker]['v'][i]
                }
        else:
            print(f"Error: {ticker} data is not in the expected dictionary format.")
    return processed_data


raw_data = extract_data(tickers_list, url, date_from, date_to)
processed_data = process_data(raw_data)