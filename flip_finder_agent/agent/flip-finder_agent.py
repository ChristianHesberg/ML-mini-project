from autogen import ConversableAgent
from flip_finder_agent.config import LLM_CONFIG
from flip_finder_agent.tools.item_list_tool import item_list
from flip_finder_agent.tools.api_reader_tool import getData
from flip_finder_agent.tools.flip_finder_tool import find_flip
from flip_finder_agent.tools.margin_calculator_tool import calculateMargin


def create_flip_finder_agent() -> ConversableAgent:
    print(LLM_CONFIG)
    # define the agent
    agent = ConversableAgent(
        name="Flip_Finder_Agent",
        system_message="You are a helpful AI assistant. "
                      "You can perform find safe and profitable flips on items in the MMORPG Old School Runescape. "
                      "A flip is buying an item at a low price and selling it at a high price. "
                      "You can find a list of items to check using the item_list tool. "
                      "You can read item data using the api_reader tool. It will return the data in this format: { 'item_id': int, 'latest_trade': {'high': int, 'highTime': int, 'low': int, 'lowTime': int}, 'timeseries': [{'timestamp': int, 'avgHighPrice': int, 'avgLowPrice': int, 'highPriceVolume': int, 'lowPriceVolume': int}] }. "
                      "You can use the 'latest_trade' dictionary received from the api to determine the trade margin on an item using the margin_calculator tool. "
                      "You should only provide the latest_trade dictionary as the input parameter. Example: calculateMargin({'high': int, 'highTime': int, 'low': int, 'lowTime': int}). "
                      "You can use the 'latest_trade' dictionary as well as the 'timeseries' list received from the api to determine if a flip is safe using the flip_finder tool. "
                      "You should only provide the 'latest_trade' dictionary and 'timeseries' list as the input parameters. Example: findFlip({'high': int, 'highTime': int, 'low': int, 'lowTime': int}, [{'timestamp': int, 'avgHighPrice': int, 'avgLowPrice': int, 'highPriceVolume': int, 'lowPriceVolume': int}])."
                      "After determining the trade margin and the safety of a flip, respond with in the following format: "
                      "{ 'item_id': int, 'safe': boolean, 'margin': int, 'buy_price': int, 'sell_price': int }"
                      "Don't include any other text in your response. "
                      "Return 'TERMINATE' when the task is done.",
        llm_config=LLM_CONFIG,
    )

    # add the tools to the agent
    agent.register_for_llm(name="item_list", description="Read item list")(item_list)
    agent.register_for_llm(name="api_reader", description="Read item data")(getData)
    agent.register_for_llm(name="margin_calculator", description="Calculate margin on item")(calculateMargin)
    agent.register_for_llm(name="flip_finder", description="Find a safe and profitable flip")(find_flip)

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
    user_proxy.register_for_execution(name="margin_calculator")(calculateMargin)
    user_proxy.register_for_execution(name="flip_finder")(find_flip)
    return user_proxy


def main():
    user_proxy = create_user_proxy()
    feedback_analysis_agent = create_flip_finder_agent()
    user_proxy.initiate_chat(
        feedback_analysis_agent,
        message="""
                1. Read items from the item list, using the item_list tool.
                2. For each item, fetch the data of the item using the api_reader tool.
                3. For each item, determine the margin of the item using the margin_calculator tool.
                4. For each item, determine the safety of the item using the flip_finder tool.
                5. Create a JSON object that contains the item id and the analyzed flip information.
                Example:
                [
                    {"item_id": "1", "safe": false, "margin": 10000, "buy_price": 100000, "sell_price": 111000},
                    {"item_id": "2", "safe": true, "margin": 20000, "buy_price": 200000, "sell_price": 222000},
                ]
                5. Return the JSON object.
                """
    )

if __name__ == "__main__":
    main()
