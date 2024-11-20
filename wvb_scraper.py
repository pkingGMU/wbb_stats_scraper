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
### Consent Button ###

#WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'privacy-policy-notice-with-close-button-close')]")))
#wd.find_elements(By.XPATH, "//*[contains(@class, 'privacy-policy-notice-with-close-button-close')]")[1].click()

# Use JavaScript to remove the consent manager element from the page
try:
    driver.execute_script("document.getElementById('transcend-consent-manager').remove();")
    print("Consent manager removed from the page.")
except Exception as e:
    print("Error while removing consent manager: ", e)

# Find match-by-match
match_by_match_tab = driver.find_element(By.ID, "ui-id-3")

# Click on match-by-match
match_by_match_tab.click()

# Wait for the page to load
time.sleep(3)



