from typing import Dict, Any

import requests

def getTimeSeriesById(id):
    r = requests.get('https://prices.runescape.wiki/api/v1/osrs/timeseries?timestep=5m&id=' + str(id),
                     headers={'Accept': 'application/json',
                              'User-Agent': 'I am trying to create a program to quickly find good margins on items that I specify.',
                              'From': 'hesbergc@yandex.com'
                              })
    return r.json()['data'][-50:]

def getItemById(id):
    r = requests.get('https://prices.runescape.wiki/api/v1/osrs/latest?id=' + str(id),
                     headers={'Accept': 'application/json',
                              'User-Agent': 'I am trying to create a program to quickly find good margins on items that I specify.',
                              'From': 'hesbergc@yandex.com'
                              })
    return r.json()['data'][str(id)]

def getData(id: int) -> Dict[str, Any]:
    timeseries = getTimeSeriesById(id)
    latest = getItemById(id)
    return {
        "item_id": id,
        "latest_trade": latest,
        "timeseries": timeseries
    }

##print(getData(13237))
print(getTimeSeriesById(13237))
print(getItemById(13237))