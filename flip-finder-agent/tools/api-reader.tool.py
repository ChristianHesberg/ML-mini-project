import requests

def getTimeSeriesById(id):
    r = requests.get('https://prices.runescape.wiki/api/v1/osrs/timeseries?timestep=5m&id=' + str(id),
                     headers={'Accept': 'application/json',
                              'User-Agent': 'I am trying to create a program to quickly find good margins on items that I specify.',
                              'From': 'hesbergc@yandex.com'
                              })
    return r.json()

def getItemById(id):
    r = requests.get('https://prices.runescape.wiki/api/v1/osrs/latest?id=' + str(id),
                     headers={'Accept': 'application/json',
                              'User-Agent': 'I am trying to create a program to quickly find good margins on items that I specify.',
                              'From': 'hesbergc@yandex.com'
                              })
    return r.json()

print(getTimeSeriesById(13237))
print(getItemById(13237))