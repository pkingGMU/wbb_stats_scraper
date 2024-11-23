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

# Get number of games

def get_game_rows():
    return driver.find_elements(By.XPATH, "//table[@id='DataTables_Table_4']//tbody//tr")

def retrieve_table(driver, site: str):

    # Base url will always stay the same
    BASE_URL = 'https://gomason.com'

    # Site url
    FULL_URL = site

    # Wait for the page to load (you may need to adjust this time)
    time.sleep(2)  # Wait for 2 seconds to make sure the page has loaded

    # Find the second tab and click it 
    second_tab = driver.find_element(By.ID, "ui-id-2")  # Update ui id
    second_tab.click()

    ### Remove the Consent button again
    # Use JavaScript to remove the consent manager element from the page
    try:
        driver.execute_script("document.getElementById('transcend-consent-manager').remove();")
        print("Consent manager removed from the page.")
    except Exception as e:
        print("Error while removing consent manager: ", e)

    # Retrieve table using caption
    caption = driver.find_element(By.XPATH, "//caption[contains(text(),'GMU - Individual')]")

    # Get the parent table of the caption
    table = caption.find_element(By.XPATH, "ancestor::table")

    return table

game_rows = get_game_rows()

for i in range(len(game_rows)):

    row = game_rows[i]

    # Locate the clickable link (anchor <a> tag) inside the game row (tr)
    game_link = row.find_element(By.TAG_NAME, 'a')  

    # Print the URL debug
    print(f"Game {i + 1} link: {game_link.get_attribute('href')}")

    time.sleep(1)

    game_link.click()

    print(i)

    time.sleep(5)



    driver.back()

    time.sleep(5)


    ### Remove the Consent button again
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

    game_rows = get_game_rows()

    
    

driver.quit()



