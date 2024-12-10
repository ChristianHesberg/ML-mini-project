from typing import Union, Literal
from autogen import AssistantAgent
from flip_finder_agent.classes.trade_data import TradeData
from flip_finder_agent.config import LLM_CONFIG_AZURE

RISK_VALUES = {"safe", "risky"}
def find_flip(trade_data: TradeData) ->  Union[Literal["safe"], Literal["unsafe"]]:
    agent = AssistantAgent(
        name="Flip_Finder_Tool",
        system_message="You are a helpful AI assistant. "
                      "My goal is to make a profit buying items at a low price and selling them at a high price the MMORPG Old School Runescape. "
                      "Your purpose is to determine if an item is a safe to trade based on the following factors: "
                      "The current buying and selling price. The average buying and selling price for a given time interval. The volume of trades for a given time interval. "
                      "The latest_trade data will be used to determine what price I will buy and sell an item at. "
                      "The timeseries data should be used as context for how the item has been recently traded. "
                      "I don't want to buy or sell items at outlier values. If the buy or sell price in the latest_trade data varies too much from the average buy and sell prices of trades in the timeseries data, I don't want to trade the item. "
                      "You should not take into account the margin when determining the risk. "
                      "You will provide the result in the following format: '[risk]'. "
                      "Example result: safe "
                      "Example of invalid result: 'the item is not a safe investment'."
                      "Don't include any other text in your response."
                      "Return 'TERMINATE' when the task is done.",
        llm_config=LLM_CONFIG_AZURE,
    )
    reply = agent.generate_reply(
        messages=[
            {"role": "user", "content": f'analyze the safety of the flip using the latest_trade: {trade_data.latest_trade} and timeseries: {trade_data.timeseries}'}
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
