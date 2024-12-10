
# Machine learning Exam Project

For our topic, we would like to make an AI agent using autogen. The agent will work similar to a stock trading bot but will instead observe the price of items in the popular MMORPG game called Old School Runescape. The agent will pull data from the old school runescape item price api, calculate if an item has a good margin for trading, and notify the user of the item and margin.


## Packages

- [@Packages](https://github.com/ChristianHesberg/ML-mini-project/blob/main/requirements.txt)

# Setup

## 1. Setup venv
python -m venv venv

## 2. activate
|OS | bash Command |
|---|---------|
|mac & linux| source venv/bin/activate |
|windows| .\venv\Scripts\activate|

- pip install -r requirements.txt

## 3. Config

- Check the config file config.py, confirm you can use one of the existing configs or create a new using a model than you can access.

- Select the config inside the flip-finder_agent.py file 
## 4. env file
- Setup a .env file inside the root folder containing the DISCORD_BOT_TOKEN
(If random error here move the DISCORD_BOT_TOKEN to line 2)



## 5. troubleshoot
- inside api_reader_tool.py you change the data set amount in the variable datapointsAmount if running into performance issues. 

