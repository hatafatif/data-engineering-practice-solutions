import requests

from zipfile import ZipFile, error
from os import mkdir, getcwd, listdir, remove


download_uris = [
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip'
]

def extract_filename_from_uri(link):
    """
    Input: URI
    Output: Filename (Expected to be after the last appearing "/" in the URI)
    """
    seperator = 0
    for n, char in enumerate(link[::-1]):
        if char == "/": #This would be the last occuring /
            seperator = n
            break
    break_from = len(link) - seperator
    filename = link[break_from:]
    return(filename)


def main():
    print('Start of program')
    # Create 'downloads' folder if not present.
    pwd = getcwd()
    if 'downloads' not in listdir(pwd):
        mkdir(pwd + '/downloads')

    # Download all links 
    for link in download_uris:

    # Download files one by one, renaming them to the URI name using helper function
        filename = extract_filename_from_uri(link)
        print(f'Requesting file: {filename}')
        r = requests.get(link, allow_redirects=True)
        open(f"downloads/{filename}", 'wb').write(r.content)

    # Extract file from zip file
        print(f'Unzipping file: {filename}')
        try:
            with ZipFile(f"downloads/{filename}", mode='r') as archive:
                for file in archive.namelist():
                    # If file name is not csv or file name is in a subdirectory, ignore.
                    if file.split(".")[-1] == "csv" and "/" not in file:
                        archive.extract(file, path="downloads/")
        except error:
            print("Unzipping failed")

    # Remove zip file
        remove(f"downloads/{filename}") 


if __name__ == '__main__':
    main()
