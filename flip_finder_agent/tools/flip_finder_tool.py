from typing import Dict, Any

from autogen import AssistantAgent
from flip_finder_agent.config import LLM_CONFIG

def find_flip(text: Dict[str, Any]) -> str:
    agent = AssistantAgent(
        name="Flip_Finder_Tool",
        system_message="You are a helpful AI assistant whose purpose is to determine whether an item is a safe and profitable flip in the MMORPG Old School Runescape. "
                      "You can analyze the data of recent trades to determine if a flip is safe and profitable. "
                      "You will receive data in this format: { 'item_id': int, 'latest_trade': {'high': int, 'highTime': int, 'low': int, 'lowTime': int}, 'timeseries': [{'timestamp': int, 'avgHighPrice': int, 'avgLowPrice': int, 'highPriceVolume': int, 'lowPriceVolume': int}] }. "
                      "The given data consists of three parts: item_id, latest_trade, and timeseries. I will now define what the data in each individual part means. "
                      "The item_id is the id of the item. "
                      "The latest_trade is data pertaining to the most recent trade. latest_trade['high'] is the most recent high price. latest_trade['low'] is the most recent low price. latest_trade['hightime'] is the time that the high price trade was made. latest_trade['lowtime'] is the time that the low price trade was made. "
                      "The timeseries data is data pertaining to the trade data of an item during time intervals. It is an array of dictionaries. Each dictionary is data for a given time interval. "
                      "A timeseries dictionary can be described as follows: timestamp is the start time of the interval. avgHighPrice is the average high price of trades made during the interval. avgLowPrice is the average low price of trades made during the interval. highPriceVolume is the amount of trades made as a high price trade. lowPriceVolume is the amount of trades made as a low price trade. "
                      "The high price will be the price I am attempting to sell an item, and the low price will be the price I am attempting to buy an item. "
                      "Given this data, you can use the flip-finder tool to determine whether the item is a safe and profitable flip. "
                      "When determining whether a flip is profitable, keep in mind that when selling an item, I will be charged a 1% tax on the sale. So 1% of the high price should be removed from the margin. "
                      "You will provide the result in the following format: { 'item_id': int, 'safe': boolean, 'margin': int }. "
                      "Example result: { 'item_id': 1396, 'safe': true, 'margin': 45,000 }. "
                      "Example of invalid result: 'item_id 1396 is a safe flip with a margin of 45,000'."
                      "Don't include any other text in your response."
                      "Return 'TERMINATE' when the task is done.",
        llm_config=LLM_CONFIG,
    )
    reply = agent.generate_reply(
        messages=[
            {"role": "user", "content": text}
        ],
    )
    return reply["content"]
'''
    if not reply:
        raise ValueError("No reply found")

    reply_value = ""
    if isinstance(reply, dict):
        reply_content = reply["content"]
        if reply_content:
            reply_value = reply_content
        else:
            raise ValueError("No content found in the reply")
    else:
        reply_value = reply

    print(f'the reply value in the flip finder tool is: {reply_value}')
'''

