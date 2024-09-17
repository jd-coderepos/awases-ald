import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import pandas as pd
from orkg import ORKG
from getpass import getpass

def setup_session():
    session = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=1,
                    status_forcelist=[500, 502, 503, 504, 104])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def fetch_paper_details(input_file, output_file, username, password):
    # Initialize the ORKG client with credentials and a custom session for retries
    session = setup_session()
    orkg = ORKG(host="https://orkg.org", creds=(username, password), session=session)

    # Read the CSV file to get DOIs
    data = pd.read_csv(input_file)
    dois = data['paper:doi'].tolist()

    # Prepare the list for storing fetched data
    papers_data = []

    # Fetch details for each DOI and extract the required information
    for doi in dois:
        response = orkg.papers.by_doi(doi=doi)
        if response.status_code == 200 and len(response.content) > 0:
            paper = response.content[0]
            papers_data.append({
                'doi': doi,
                'paper_id': paper['id'],
                'paper_title': paper['title']
            })
        else:
            print(f"Failed to fetch data or error occurred for DOI: {doi}, Status Code: {response.status_code}")

    # Convert the list of dictionaries to a DataFrame
    output_data = pd.DataFrame(papers_data)

    # Write the DataFrame to a new CSV file
    output_data.to_csv(output_file, index=False)
    print(f"Data has been written to {output_file}")

# Input credentials and file paths from user
username = input("Enter your ORKG username: ")
password = getpass("Enter your ORKG password: ")
input_file_path = input("Enter the path of the input CSV file: ")
output_file_path = input("Enter the path of the output CSV file: ")

# Execute the function with user inputs
fetch_paper_details(input_file_path, output_file_path, username, password)
