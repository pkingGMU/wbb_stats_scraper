This project contains 2 python scripts

1. scraper.py
2. wvb_scraper.py

Scraper.py is a simple html parser that takes in a webpage and exports a csv to `Game-Stats` Folder

Instructions:
1. Download the repo
2. Ensure you have the Game-Stats folder. It should be empty
3. Run scraper.py
4. Enter in the website of a womens basketball game in the terminal when prompted (Ex. https://gomason.com/sports/womens-basketball/stats/2024-25/johnson-c-smith-university/boxscore/13176). IT MUST BE A BOX SCORE
5. Name your file in the terminal when prompted

wvb_scraper.py is run by a more complicated selenium driver as the wvb pages are dynamic javascript.
1. Download the repo
2. Ensure you have the Game-Stats folder. It should be empty
3. Run wvb_scraper.py
4. It will scrape the entire list of games
5. Each file will be named as an interation (1st game = 0_game.csv)
