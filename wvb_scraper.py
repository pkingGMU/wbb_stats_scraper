import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
from openpyxl import load_workbook


def initiate_driver():
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

    # Pass the driver to the next step
    return driver

# Get number of games

def get_game_rows(driver):
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


def format_table(table):

        # Extract the rows of the table
        rows = table.find_elements(By.TAG_NAME, 'tr')

        # Prepare a list to store the table data
        table_data = []

        # Main header row
        main_header = rows[0].find_elements(By.TAG_NAME, 'th')

        # Sub header row
        sub_header = rows[1].find_elements(By.TAG_NAME, 'th')

        headers = [
            '##', 'Player', 'SP', 'K', 'E', 'TA', 'Pct', 'A', 'E_2', 'SA', 'SE', 'BS', 'BA', 'BE', 'DIG', 'BHE', 'RE', 'Pts'
        ]

        # Extract the data rows skipping the first 2 header rows and not including the last
        for row in rows[2:-1]:  # Skip the header row
            columns = row.find_elements(By.TAG_NAME, 'td')
            if len(columns) > 0:  # Make sure this is not an empty row
                row_data = [col.text.strip() for col in columns if col.text.strip() != '']
                table_data.append(row_data)

        # Create a pandas DataFrame from the table data
        df = pd.DataFrame(table_data, columns=headers)

        exclude_column = 'Player'

        # Convert all columns except the specified one to numeric (if possible)
        for col in df.columns:
            if col != exclude_column:
                

                df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert all to numeric except the excluded column


        return df

def export_df(df, i):

    if f'master.xlsx' in os.listdir(f'Game-Stats') and i == 0:
        os.remove(f"Game-Stats/master.xlsx")

    if f'master.xlsx' in os.listdir(f'Game-Stats'):

        with pd.ExcelWriter(f"Game-Stats/master.xlsx", engine='openpyxl', mode='a') as writer:  
            df.to_excel(writer, sheet_name=f"Game-{i}", index=False)
    else:
        df.to_excel(f"Game-Stats/master.xlsx", engine='openpyxl', index=False, sheet_name=f"Game-{i}")
    

    # Save the DataFrame to a CSV file in the "Game-Stats" folder
    df.to_csv(f"Game-Stats/{i}.csv", index=False)

def main():

    # Create driver
    driver = initiate_driver()

    # Get the game rows
    game_rows = get_game_rows(driver)

    selection = input(f'Would you like to process all games or only a few? Type all or a specified number: ')

    if selection.lower() == 'all':
        cycles = len(game_rows)
    else:
        cycles = int(selection)

    # Cycle through each game
    for i in range(cycles):

        row = game_rows[i]

        # Locate the clickable link (anchor <a> tag) inside the game row (tr)
        game_link = row.find_element(By.TAG_NAME, 'a')  

        # Define site string
        site = game_link.get_attribute('href')

        # Print the URL debug
        print(f"Game {i + 1} link: {site}")

        # Sleep for loading
        time.sleep(1)

        # Click link to individual game
        game_link.click()

        # Debugging
        print(i)

        # Sleep for loading
        time.sleep(5)

        # Retrieve table function
        table = retrieve_table(driver, site)

        # Format the table
        df = format_table(table)

        # Export the table
        export_df(df, i)

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

        game_rows = get_game_rows(driver)

    
    

    driver.quit()

if __name__ == '__main__':
    main()



