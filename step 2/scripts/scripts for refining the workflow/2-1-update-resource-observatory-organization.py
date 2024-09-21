import pandas as pd
from orkg import ORKG
from getpass import getpass

def read_resources_from_csv(file_path):
    """ Read the CSV file containing resource information. """
    return pd.read_csv(file_path)

def update_resources(orkg, data, new_obs, new_org):
    """ Update the observatory and organization for each resource. """
    for _, row in data.iterrows():
        if row['Status'] == 'Processed':  # Assuming you only want to update 'Processed' resources
            try:
                response = orkg.resources.update_observatory(
                    id=str(row['ORKG Resource ID']), 
                    observatory_id=str(new_obs), 
                    organization_id=str(new_org)
                )
                response_content = response.content  # Get the response content
                print(f"Updated Resource {row['Name']} with ID {row['ORKG Resource ID']}: {response_content}")
            except Exception as e:
                print(f"Failed to update Resource {row['Name']} with ID {row['ORKG Resource ID']}: {e}")

def main():
    host_address = input("Enter the ORKG host address: ")
    email = input("Enter your ORKG email address: ")
    password = getpass("Enter your ORKG password: ")
    input_file_path = input("Enter the path of the input CSV file: ")
    new_obs = input("Enter the new observatory ID: ")
    new_org = input("Enter the new organization ID: ")

    orkg = ORKG(host=host_address, creds=(email, password))
    resource_data = read_resources_from_csv(input_file_path)
    update_resources(orkg, resource_data, new_obs, new_org)

if __name__ == "__main__":
    main()
