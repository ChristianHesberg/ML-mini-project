import asyncio
import os

import discord
from autogen import ConversableAgent
from dotenv import load_dotenv

from flip_finder_agent.config import LLM_CONFIG
from flip_finder_agent.tools.discord_bot_tool import send_flip
from flip_finder_agent.tools.item_list_tool import item_list
from flip_finder_agent.tools.api_reader_tool import getData
from flip_finder_agent.tools.flip_finder_tool import find_flip

def create_flip_finder_agent() -> ConversableAgent:
    print(LLM_CONFIG)
    # define the agent
    agent = ConversableAgent(
        name="Flip_Finder_Agent",
        system_message="You are a helpful AI assistant. "
                      "My goal is to make a profit buying items at a low price and selling them at a high price the MMORPG Old School Runescape. "
                      "You can find a list of items to check using the item_list tool. "
                      "You can read data of an item using the api_reader tool. It will return a class TradeData that contains 'latest_trade' and 'timeseries' fields. "
                      "The 'latest_trade' field is a LatestTrade class that contains information about the latest trade. "
                      "The 'timeseries' field is a list of TimeInterval classes that contains trade information about the item for a time interval. "
                      "Given a TradeData, you can analyze if an item is a safe trade using the flip_finder tool. "
                      "Don't include any other text in your response. "
                      "Return 'TERMINATE' when the task is done.",
        llm_config=LLM_CONFIG,
    )

    # add the tools to the agent
    agent.register_for_llm(name="item_list", description="Read item list")(item_list)
    agent.register_for_llm(name="api_reader", description="Read item data")(getData)
    agent.register_for_llm(name="flip_finder", description="Analyze if a trade on an item is safe")(find_flip)
    agent.register_for_llm(name="discord_bot", description="Sends message to discord with flip")(send_flip)
    return agent

def create_user_proxy():
    user_proxy = ConversableAgent(
        name="User",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
    )
    user_proxy.register_for_execution(name="item_list")(item_list)
    user_proxy.register_for_execution(name="api_reader")(getData)
    user_proxy.register_for_execution(name="flip_finder")(find_flip)
    user_proxy.register_for_execution(name="discord_bot")(send_flip)
    return user_proxy


def main():
    user_proxy = create_user_proxy()
    feedback_analysis_agent = create_flip_finder_agent()
    user_proxy.initiate_chat(
        feedback_analysis_agent,
        message="""
                1. Read items from the item list, using the item_list tool.
                2. For each item, fetch the data of the item using the api_reader tool.
                3. For each item, determine the safety of trading the item using the flip_finder tool.
                4. Create a stringified JSON object that contains the item id and the analyzed flip information needed for making the trade.
                Example:
                [
                    {"item_id": "1", "safe": false, "margin": 10000, "buy_price": 100000, "sell_price": 111000},
                    {"item_id": "2", "safe": true, "margin": 20000, "buy_price": 200000, "sell_price": 222000},
                ]
                5. Send the stringified JSON object to discord using the discord_bot send_flip method.
                6. Return the JSON object.
                """
    )

if __name__ == "__main__":
    main()
