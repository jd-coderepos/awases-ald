import csv
import getpass  # Import getpass module for secure password input
from orkg import ORKG

def read_resource_ids(input_file):
    resource_ids = []
    with open(input_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Assuming the header "contribution resource id" is the last column
            resource_id = row['contribution resource id']
            resource_ids.append(resource_id)
    return resource_ids

def process_resource_ids(orkg_host, orkg_email, orkg_password, resource_ids):
    orkg = ORKG(host=orkg_host, creds=(orkg_email, orkg_password))
    # Placeholder function to process each resource ID
    for resource_id in resource_ids:
        print(f"Processing resource ID: {resource_id}")
        # Add your specific processing code here
        if orkg.resources.exists(id=resource_id):
            orkg.resources.delete(id=resource_id)
        else:
            print("resource does not exit")

if __name__ == "__main__":
    # Prompt user for input file path
    input_file = input("Please enter the path to the input CSV file: ").strip()
    orkg_host = input("Enter ORKG host URL: ")
    orkg_email = input("Enter your ORKG email: ")
    orkg_password = getpass.getpass("Enter your ORKG password: ")  # Secure password input    
    
    try:
        resource_ids = read_resource_ids(input_file)
        process_resource_ids(orkg_host, orkg_email, orkg_password, resource_ids)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except KeyError:
        print(f"Error: The file '{input_file}' does not have the required header 'contribution resource id'.")
    except Exception as e:
        print(f"An error occurred: {e}")
