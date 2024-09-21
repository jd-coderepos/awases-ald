import pandas as pd
import json
from orkg import ORKG, OID
import getpass  # Import getpass module for secure password input
import os

def read_mapping(file_path):
    mapping_df = pd.read_csv(file_path)
    return {row['Name']: row['ORKG Resource ID'] for index, row in mapping_df.iterrows()}

def create_contribution(data, contribution_id, template, reactant_mapping, material_mapping):
    process_parameters = data.get('process_parameters', {})
    film_properties = data.get('film_properties', {})
    process_characteristics = data.get('process_characteristics', {})
    
    # Get the reactants, which is assumed to be a list potentially containing a single string of comma-separated values
    reactant_string = process_parameters.get('reactants', [''])[0]

    # Split the string on commas, strip whitespace, and convert each valid reactant using the reactant_mapping and OID
    reactants = [
        OID(reactant_mapping[reactant.strip()]) for reactant in reactant_string.split(',')
        if reactant.strip() in reactant_mapping
    ]
    
    # Map material name to ORKG Resource ID
    material = OID(material_mapping.get(film_properties.get('material', ''), film_properties.get('material', '')))
    
    # Create an instance of the template with the extracted data
    instance = template.comprehensive_ald_profile(
        label=f"Contribution {contribution_id}",
        process_parameter=template.ald_process_parameters(
            reactant=reactants,
            temperature_range=process_parameters.get('temperature_range', ""),
            pressure_range=process_parameters.get('pressure_range', "")
        ),
        film_property=template.ald_film_properties(
            material=material,
            thickness_control=film_properties.get('thickness_control', ""),
            conformality=film_properties.get('conformality', ""),
            film_thickness=film_properties.get('film_thickness', ""),
            film_density=film_properties.get('film_density', ""),
            surface_roughness=film_properties.get('surface_roughness', ""),
            refractive_index=film_properties.get('refractive_index', "")
        ),
        process_characteristic=template.ald_process_characteristics(
            self_limiting_behavior=process_characteristics.get('self_limiting_behavior', ""),
            growth_per_cycle=process_characteristics.get('growth_per_cycle', "")
        )
    )
    
    return instance

def append_record_to_csv(record, output_file_path):
    # Check if the file exists, and create it if not
    if not os.path.exists(output_file_path):
        # Create the file with a header if it does not exist
        pd.DataFrame([record]).to_csv(output_file_path, index=False)
    else:
        # Append the record to the existing file
        pd.DataFrame([record]).to_csv(output_file_path, mode='a', header=False, index=False)

def main(file_path, orkg_host, orkg_email, orkg_password, template_resource_id, output_file_path, reactant_mapping_path, material_mapping_path):
    # Initialize ORKG client with user inputs
    orkg = ORKG(host=orkg_host, creds=(orkg_email, orkg_password))
    
    # Materialize the specified template
    orkg.templates.materialize_template(template_resource_id)

    template = orkg.templates
    
    # Read CSV file and mappings
    data = pd.read_csv(file_path)
    reactant_mapping = read_mapping(reactant_mapping_path)
    material_mapping = read_mapping(material_mapping_path)
    
    # Track contributions per paper
    paper_contributions = {}
    
    # Iterate through each row of data
    for index, row in data.iterrows():
        paper_id = row['paper_id']
        
        # Reset contribution counter for each new paper
        if paper_id not in paper_contributions:
            paper_contributions[paper_id] = 0
        
        contribution_id = paper_contributions[paper_id] + 1
        paper_contributions[paper_id] = contribution_id
        
        extracted_info = json.loads(row['extracted_info'])

        # Ask user for confirmation before saving the contribution
        confirmation = input(f"Do you want to save Contribution {contribution_id} for Paper ID {paper_id}? (yes/no): ").strip().lower()
        
        # Check user's confirmation response
        if confirmation in ['no', 'n']:
            print("Exiting workflow as requested.")
            return  # Exit the entire workflow
        elif confirmation not in ['yes', 'y']:
            print(f"Skipping Contribution {contribution_id} for Paper ID {paper_id}.")
            continue

        # Create a new contribution
        contribution = create_contribution(extracted_info, contribution_id, template, reactant_mapping, material_mapping)
        contribution_response = contribution.save()  # Saving the contribution
        contribution_resource_id = contribution_response.content['id']  # Extracting contribution resource ID
        print("contribution response:"+contribution_response)
        
        # Logging information for saved contribution
        print(f"Contribution {contribution_id} for Paper ID {paper_id} saved successfully with Contribution Resource ID: {contribution_resource_id}")

        # Prepare paper data and add to ORKG
        paper_data = {
            "predicates": [],
            "paper": {
                "title": row['paper_title'],
                "researchField": "R254",
                "contributions": [contribution.template_dict['resource']]
            }
        }
        
        paper_response = orkg.papers.add(params=paper_data, merge_if_exists=True)
        print("paper response: "+paper_response)
        
        # Logging information for paper addition
        print(f"Contribution {contribution_id} added to Paper ID {paper_id}. Paper Response: {paper_response.content}")

        # Process response and append record to CSV file
        record = {
            "contribution id": contribution_id,
            "paper title": row['paper_title'],
            "paper id": paper_id,  # Using paper_id directly from the input file
            "contribution resource id": contribution_resource_id  # Contribution resource ID from the response
        }
        
        append_record_to_csv(record, output_file_path)
        
    print("Data uploaded and recorded successfully.")

if __name__ == "__main__":
    orkg_host = input("Enter ORKG host URL: ")
    orkg_email = input("Enter your ORKG email: ")
    orkg_password = getpass.getpass("Enter your ORKG password: ")  # Secure password input
    template_resource_id = input("Enter the resource ID of the template to materialize: ")
    csv_file_path = input("Enter the path to your CSV file: ")
    output_file_path = input("Enter the path for the output CSV file: ")
    reactant_mapping_path = input("Enter the path to the reactant mapping CSV file: ")
    material_mapping_path = input("Enter the path to the material mapping CSV file: ")
    
    main(csv_file_path, orkg_host, orkg_email, orkg_password, template_resource_id, output_file_path, reactant_mapping_path, material_mapping_path)
