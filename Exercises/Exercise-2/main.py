import pandas as pd
import requests
from bs4 import BeautifulSoup

# Note: This script was written assuming that only 1 file with a Last Modified was supposed to be downloaded. Since there are more than one files with 
# the same last modified, I need to add functionality to the code to download all files with the same name, and then do the same process for every file. 

URL = 'https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/'

def main():
    # Get request to base URL
    r = requests.get(URL)

    # Using bs4 library to parse HTML
    soup = BeautifulSoup(r.content)

    # Finding all 'tr' elements
    rows = soup.find_all('tr')

    # Searching for the required row from the given input
    for row in rows:
        if len(row.findAll('td')) < 2:
            continue
        if "2022-02-07 14:03" in row.findAll('td')[1].text:
            target_row = row
            break

    # Extracting filename from the selected row
    target_filename = target_row.find('a').text

    # Creating URL for downloading the file
    file_url = f'{URL}{target_filename}'

    # Second request to download required file
    r2 = requests.get(file_url)
    open(target_filename, 'wb').write(r2.content)

    # Using pandas to open csv file
    df = pd.read_csv(target_filename)

    # Finding max value from HourlyDryBulbTemperature column
    max = pd.to_numeric(df['HourlyDryBulbTemperature'], errors='coerce').describe().loc['max']

    # Selecting rows where value matches the max
    target_rows = df[pd.to_numeric(df['HourlyDryBulbTemperature'], errors='coerce') == max]

    # Final print to the console
    print(f'Rows with highest HourlyDryBulbTemperature are: {list(target_rows.index)}')



if __name__ == '__main__':
    main()