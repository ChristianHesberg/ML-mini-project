from flip_finder_agent.classes.latest_trade import LatestTrade

def calculateMargin(latest_trade: LatestTrade) -> LatestTrade:
    high = latest_trade.sell_price
    low = latest_trade.buy_price
    margin = high - low - high * 0.01
    latest_trade.margin = round(margin)
    return latest_trade
