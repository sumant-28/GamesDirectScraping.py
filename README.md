# GamesDirectScraping.py

At the time of writing next generation gaming consoles (Xbox Series S/X and PS5) are hard to acquire due to scalping and supply chain issues. This project 
aims at coming up with a consumer-focused solution to the task of acquiring one of these home electronics goods through web scraping.
The online store being scraped arranges all of the items it sells in a json file. By interrogating the tags and performing keyword searches
a target database in SQLite that contains the items of interest can be created for continuous monitoring. These databases can be automated to be 
run periodically. Commands in the script print statements to the terminal alerting of changes to stock. The database also holds useful static information
about when inventory is created, published and updated to get a signal of how high demand is.
