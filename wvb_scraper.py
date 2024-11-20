import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
# Create driver from selenium
driver = webdriver.Firefox()

# Get stats page of Womens Volleyball
url = 'https://gomason.com/sports/womens-volleyball/stats'
driver.get(url)

time.sleep(3)


