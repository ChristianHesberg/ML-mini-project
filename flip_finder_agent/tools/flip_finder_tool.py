from typing import Dict, Any, List, Union, Literal

from autogen import AssistantAgent
from flip_finder_agent.config import LLM_CONFIG

RISK_VALUES = {"safe", "unsafe"}
def find_flip(latest_trade: Dict[str, int], timeseries: List[Dict[str, int]]) ->  Union[Literal["safe"], Literal["unsafe"]]:
    agent = AssistantAgent(
        name="Flip_Finder_Tool",
        system_message="You are a helpful AI assistant. "
                      "Your purpose is to determine if an item is a safe flip in the MMORPG Old School Runescape."
                      "You can analyze the data of recent trades to determine if a flip is safe. "
                      "The latest_trade parameter will be in this format: {'high': int, 'highTime': int, 'low': int, 'lowTime': int}. "
                      "The latest_trade keys are defined as follows: 'high' is the sell price of the item. 'highTime' is a Unix timestamp indicating the last time the item was sold at the 'high' price. 'low' is the buy price of the item. 'lowTime' is a Unix timestamp indicating the last time the item was sold at the 'low' price. "
                      "The timeseries parameter will be in this format: [{'timestamp': int, 'avgHighPrice': int, 'avgLowPrice': int, 'highPriceVolume': int, 'lowPriceVolume': int}]. "
                      "The timeseries parameter is a list containing dictionaries, where each dictionary corresponds to data of a time interval. "
                      "The keys in the time interval dictionaries are defined as follows: 'timestamp' is the start time of the time interval. 'avgHighPrice' is the average selling price of the item during the time interval. 'avgLowPrice' is the average buying price of the item during the time interval. 'highPriceVolume' is the amount of items sold at the sell price during the time interval. 'lowPriceVolume' is the amount of items bought at the buy price during the time interval. "
                      "The latest_trade data will be used to determine what price I will buy and sell an item at. "
                      "You should use the timeseries data to determine if a flip is stable, and if it is safe to buy and sell at the price determined from the latest_trade data. "
                      "You will provide the result in the following format: '[risk]'. "
                      "Example result: 'safe'. "
                      "Example of invalid result: 'the item is not a safe investment'."
                      "Don't include any other text in your response."
                      "Return 'TERMINATE' when the task is done.",
        llm_config=LLM_CONFIG,
    )
    reply = agent.generate_reply(
        messages=[
            {"role": "user", "content": {latest_trade, timeseries}}
        ],
    )

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

    reply_values = reply_value.splitlines()
    if len(reply_values) != 1:
        filtered_lines = list(filter(lambda x: RISK_VALUES.intersection(set(x.lower().split())), reply_values))
        reply_value = filtered_lines[0] if filtered_lines else ""

    reply_value = reply_value.replace("[", "").replace("]", "").replace(" ", "").strip()

    if reply_value not in RISK_VALUES:
        raise ValueError(f"Invalid risk value: {reply_value}")

    return reply_value
