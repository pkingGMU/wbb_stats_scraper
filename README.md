
# WBB_STATS_SCRAPER

This is a project meant for retrieving individual player stats from the wbb team




## About

This project contains 2 python scripts

1. scraper.py
2. wvb_scraper.py


## Installation - wbb

Scraper.py is a simple html parser that takes in a webpage and exports a csv to `Game-Stats` Folder



```bash
    1. Download the repo
    3. Create a virtual environment
    4. Add forge config for conda, $ conda config --append channels conda-forge
    5. Install the requirements by typing in your terminal, $ conda install --file requirements.txt
    6. Ensure you have the Game-Stats folder. It should be empty
    7. Run scraper.py
    8. Enter in the website of a womens basketball game in the terminal when prompted (Ex. https://gomason.com/sports/womens-basketball/stats/2024-25/johnson-c-smith-university/boxscore/13176). IT MUST BE A BOX SCORE
    9. Name your file in the terminal when prompted
```


## Installation - wvb

wvb_scraper.py is run by a more complicated selenium driver as the wvb pages are dynamic javascript.


```bash
    Instructions:
    1. Download the repo
    2. Install the requirements by typing in your terminal, conda install --file requirements.txt
    3. Ensure you have the Game-Stats folder. It should be empty
    4. Run wvb_scraper.py
    5. It will scrape the entire list of games
    6. Each file will be named as an interation (1st game = 0_game.csv)
    
