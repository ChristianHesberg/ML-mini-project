from autogen import ConversableAgent
from flip_finder_agent.config import LLM_CONFIG
from flip_finder_agent.tools.item_list_tool import item_list
from flip_finder_agent.tools.api_reader_tool import getData
from flip_finder_agent.tools.flip_finder_tool import find_flip

def create_flip_finder_agent() -> ConversableAgent:
    print(LLM_CONFIG)
    # define the agent
    agent = ConversableAgent(
        name="Flip Finder Agent",
        system_message="You are a helpful AI assistant. "
                      "You can perform find safe and profitable flips on items in the MMORPG Old School Runescape. "
                      "You can find a list of items to check using the item-list tool. "
                      "You can read item data using the api-reader tool. It will return the data in this format: { 'item_id': number, 'latest_trade': {'high': number, 'highTime': number, 'low': number, 'lowTime': number}, 'timeseries': [{'timestamp': number, 'avgHighPrice': number, 'avgLowPrice': number, 'highPriceVolume': number, 'lowPriceVolume': number}] }. "
                      "You can calculate a safe and profitable flip using the flip-finder tool. It will expect data in the format given by the api-reader tool. It will return the data in this format: { 'item_id': number, 'safe': boolean, 'margin': number }. "
                      "Don't include any other text in your response. "
                      "Return 'TERMINATE' when the task is done.",
        llm_config=LLM_CONFIG,
    )

    # add the tools to the agent
    agent.register_for_llm(name="item_list", description="Read item list")(item_list)
    agent.register_for_llm(name="api_reader", description="Read item data")(getData)
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
                3. Use the data for each item to determine whether the item is a safe and profitable flip using the flip_finder tool.
                4. Return the JSON object.
                """
    )

if __name__ == "__main__":
    main()
