from typing import Dict
def calculateMargin(price_info: Dict[str, int]):
    high = price_info["high"]
    low = price_info["low"]
    margin = high - low - high * 0.01
    price_info["margin"] = round(margin)
    return price_info

