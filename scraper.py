import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page to scrape
url = 'https://gomason.com/sports/womens-basketball/stats/2024-25/towson-university/boxscore/13177'

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    print("Successfully accessed the page!")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
    exit()

# Parse the content of the page with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table with the stats (based on the table structure)
# Looking for a table with a specific class or ID related to GMU player stats
# We need to inspect the HTML structure of the page to find the correct table

# In this case, we can search for a table with 'boxscore' in its class (from inspecting the page)
h3 = soup.find('h3', string=lambda t: 'George Mason' in t)

# If an h3 is found, get its next sibling table
if h3:
    table = h3.find_next('table')

# If we successfully found the table
if table:
    # Extract the rows of the table
    rows = table.find_all('tr')
    
    # Prepare to store the player data
    player_data = []

    # Iterate through each row and extract player stats
    for row in rows:
        columns = row.find_all('td')
        if len(columns) > 0:  # Ignore header or empty rows
            player_stats = [col.text.strip() for col in columns]
            player_data.append(player_stats)

    # Convert the player data into a DataFrame for easier analysis
    column_headers = [
        "##", "Player", "GS", "MIN", "FG", "3PT", "FT", "ORB-DRB", "REB", 
        "PF", "A", "TO", "BLK", "STL", "PTS"
    ]
    
    # Create a DataFrame
    df = pd.DataFrame(player_data, columns=column_headers)

    # Delete rows 12 and 13
    df = df.drop([12, 13]).reset_index(drop=True)


    # Remove everything up until the first space in the 'Player' column
    df['Player'] = df['Player'].str.replace(r'^\d+\s+', '', regex=True)

    # Sort the DataFrame by the 'Player' column in alphabetical order
    df = df.sort_values(by='Player', ascending=True).reset_index(drop=True)

    print(df)

    # Split columns (3PT, FG, FT, ORB-DRB)
    for col in ['FG', '3PT', 'FT', 'ORB-DRB']:

        if col == 'ORB-DRB':
            df[[f'ORB', f'DRB']] = df[col].str.split('-', expand=True)
        else:
            df[[f'{col} Made', f'{col} Attempt']] = df[col].str.split('-', expand=True)

    print(df)

    #Convert columns to numeric values (attempts and made)
    for col in ['FG', '3PT', 'FT']:
        df[f'{col} Made'] = pd.to_numeric(df[f'{col} Made'])
        df[f'{col} Attempt'] = pd.to_numeric(df[f'{col} Attempt'])

    print(df)
    
    # Calculate percentages (e.g., 3PT%, FG%, FT%, ORB%)
    df['3PT%'] = (df['3PT Made'] / df['3PT Attempt']).fillna(0) * 100
    df['FG%'] = (df['FG Made'] / df['FG Attempt']).fillna(0) * 100
    df['FT%'] = (df['FT Made'] / df['FT Attempt']).fillna(0) * 100
    
    # Debug 
    print(df.columns.tolist())

    # Reorder

    col_order = ["##", "Player", "FG Made", "FG Attempt", "FG%", "3PT Made", "3PT Attempt", "3PT%", "FT Made", "FT Attempt", "FT%", "ORB", "DRB", "REB", 
        "PF", "A", "TO", "BLK", "STL", "PTS" ]
    
    # Reorder the columns based on the defined order
    df = df[col_order]

    df = round(df, 2)

    file_name = input("Enter the name of the file: ")

    # Save the DataFrame to a CSV file in the "Game-Stats" folder
    df.to_csv(f"Game-Stats/{file_name}.csv", index=False)

    # Print the DataFrame
    print(df)
else:
    print("Could not find the player stats table on the page.")