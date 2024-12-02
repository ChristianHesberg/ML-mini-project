from typing import Annotated
from pydantic import BaseModel, Field

class TimeInterval(BaseModel):
    timestamp: Annotated[int, Field(description="Unix timestamp indicating the start time of the interval.")]
    average_sell_price: Annotated[int | None, Field(description="The average selling price of the item over the time interval.")]
    average_buy_price: Annotated[int | None, Field(description="The average buying price of the item over the time interval.")]
    sell_price_volume: Annotated[int, Field(description="The amount of trades made at the selling price.")]
    buy_price_volume: Annotated[int, Field(description="The amount of trades made at the buying price.")]
    # def __init__(self, timestamp: int, average_sell_price: int, average_buy_price: int, sell_price_volume: int, buy_price_volume: int):
    #     self.buy_price_volume = buy_price_volume
    #     self.sell_price_volume = sell_price_volume
    #     self.average_buy_price = average_buy_price
    #     self.average_sell_price = average_sell_price
    #     self.timestamp = timestamp

