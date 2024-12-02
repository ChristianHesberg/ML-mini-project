from typing import Dict
def calculateMargin(latest_trade: Dict[str, Dict[str, int]]) -> Dict[str, int]:
    price_info = latest_trade["latest_trade"]
    high = price_info["high"]
    low = price_info["low"]
    margin = high - low - high * 0.01
    price_info["margin"] = round(margin)
    return price_info
