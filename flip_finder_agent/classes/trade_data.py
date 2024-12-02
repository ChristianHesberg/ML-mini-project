from typing import List, Annotated

from pydantic import Field, BaseModel

from flip_finder_agent.classes.latest_trade import LatestTrade
from flip_finder_agent.classes.time_interval import TimeInterval


class TradeData(BaseModel):
    latest_trade: Annotated[LatestTrade, Field(description="Data on the most recent trade of an item. ")]
    timeseries: Annotated[List[TimeInterval], Field(description="A list of time interval data. ")]
    # def __init__(self, latest_trade: LatestTrade, timeseries: List[TimeInterval]):
    #     self.latest_trade = latest_trade
    #     self.timeseries = timeseries