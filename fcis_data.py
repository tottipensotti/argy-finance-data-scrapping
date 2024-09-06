from datetime import datetime, timedelta
from typing import List
import requests

days_to_calculate: int = 7

last_workday: datetime = datetime.now()
while last_workday.weekday() > 4:
    last_workday = last_workday - timedelta(days=1)
last_workday = last_workday-timedelta(days=1)

dates: List[str] = [
  date.isoformat().split('T') for date in  [
    last_workday - timedelta(days=x)
    for x in range(days_to_calculate)
  ]
]

urls = [f'https://api.cafci.org.ar/estadisticas/informacion/diaria/4/{date[0]}' for date in dates]
data = {}
for date, url in zip(dates, urls):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data[date[0]] = response.json()['data']
        except KeyError: # When is a weekend the json has no 'data' as the markets are closed.
            data[date[0]] = None
        print(f'Request to {url} for date {date[0]} was successful.')
    else:
        print(f'Request to {url} for date {date[0]} failed with status code {response.status_code}.')
