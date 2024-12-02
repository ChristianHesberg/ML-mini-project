from typing import Annotated

from pydantic import Field, BaseModel


class LatestTrade(BaseModel):
    sell_price: Annotated[int, Field(description="The selling price of the item.")]
    sell_price_time: Annotated[int, Field(description="Unix timestamp indicating when the item was sold at the selling price.")]
    buy_price: Annotated[int, Field(description="The buying price of the item.")]
    buy_price_time: Annotated[int, Field(description="Unix timestamp indicating when the item was sold at the buying price")]
    margin: Annotated[int | None, Field(description="The profit margin on the item if sold at the selling price and bought at the buying price. ")]
    # def __init__(self, sell_price: int, sell_price_time: int, buy_price: int, buy_price_time: int, margin: int | None):
    #     self.sell_price = sell_price
    #     self.sell_price_time = sell_price_time
    #     self.buy_price = buy_price
    #     self.buy_price_time = buy_price_time
    #     self.margin = margin