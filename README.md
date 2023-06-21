# EDLT-bot

EDLT-bot is a discord bot paired with a simple website scraper to help EDLT company employees easily access data about their routes.

The scraper.py file pulls the JSON data from the amazon.logistics website. It then removes the unused info and sorts the data with the highest delivery completion rate at the top.

The bot.py file calls the scraper file and then uses the data provided to send a formatted version of the data to a discord server. 

EDLT company employees have access the the discord server and are able to retrieve info about their routes using bot commands such as, "!driverid" and "!driverinfo".
