from typing import List

import requests

from flip_finder_agent.classes.latest_trade import LatestTrade
from flip_finder_agent.classes.time_interval import TimeInterval
from flip_finder_agent.classes.trade_data import TradeData
from flip_finder_agent.tools.margin_calculator_tool import calculateMargin


def getTimeSeriesById(id: int) -> List[TimeInterval]:
    r = requests.get('https://prices.runescape.wiki/api/v1/osrs/timeseries?timestep=5m&id=' + str(id),
                     headers={'Accept': 'application/json',
                              'User-Agent': 'I am trying to create a program to quickly find good margins on items that I specify.',
                              'From': 'hesbergc@yandex.com'
                              })
    res = []
    for item in r.json()['data'][-50:]:
        time_interval = TimeInterval(timestamp=item['timestamp'], average_sell_price=item['avgHighPrice'], average_buy_price=item['avgLowPrice'], sell_price_volume=item['highPriceVolume'], buy_price_volume=item['lowPriceVolume'])
        res.append(time_interval)
    return res

def getItemById(id: int) -> LatestTrade:
    r = requests.get('https://prices.runescape.wiki/api/v1/osrs/latest?id=' + str(id),
                     headers={'Accept': 'application/json',
                              'User-Agent': 'I am trying to create a program to quickly find good margins on items that I specify.',
                              'From': 'hesbergc@yandex.com'
                              })
    res = r.json()['data'][str(id)]
    latest_trade = LatestTrade(sell_price=res['high'], sell_price_time=res['highTime'], buy_price=res['low'], buy_price_time=res['lowTime'], margin=None)
    return calculateMargin(latest_trade)

def getData(id: int) -> TradeData:
    timeseries = getTimeSeriesById(id)
    latest = getItemById(id)
    return TradeData(latest_trade=latest, timeseries=timeseries)

##print(getData(13237))
print(getTimeSeriesById(13237))
print(getItemById(13237))