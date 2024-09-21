import pandas as pd
import json
from orkg import ORKG, OID
import getpass  # Import getpass module for secure password input
import os

def read_mapping(file_path):
    mapping_df = pd.read_csv(file_path)
    return {row['Name']: row['ORKG Resource ID'] for index, row in mapping_df.iterrows()}

def get_valid_param(param_dict, key):
    """ Helper to get valid parameters. Returns None if the parameter is '-', empty, or NaN. """
    value = param_dict.get(key, '')
    if pd.isna(value) or value in ['-', '']:
        return None
    return value

def create_contribution(data, contribution_id, template, reactant_mapping, material_mapping):
    process_parameters = data.get('process_parameters', {})
    film_properties = data.get('film_properties', {})
    process_characteristics = data.get('process_characteristics', {})

    reactant_string = process_parameters.get('reactants', [''])[0]
    reactants = [
        OID(reactant_mapping[reactant.strip()]) for reactant in reactant_string.split(',')
        if reactant.strip() in reactant_mapping
    ]
    primary_reactant = reactants[0] if reactants else None
    additional_reactants = reactants[1:]  # Remaining reactants after the first

    material = OID(material_mapping.get(film_properties.get('material', ''), film_properties.get('material', '')))

    # Build process parameters conditionally
    process_params = {}
    if primary_reactant is not None:
        process_params['reactant'] = primary_reactant
    temp_range = get_valid_param(process_parameters, 'temperature_range')
    if temp_range is not None:  # Explicit check for None
        process_params['temperature_range'] = temp_range
    press_range = get_valid_param(process_parameters, 'pressure_range')
    if press_range is not None:  # Explicit check for None
        process_params['pressure_range'] = press_range

    # Build film properties conditionally
    film_props = {}
    for key in ['thickness_control', 'conformality', 'film_thickness', 'film_density', 'surface_roughness', 'refractive_index']:
        value = get_valid_param(film_properties, key)
        if value is not None:
            film_props[key] = value
    if material:
        film_props['material'] = material

    # Build process characteristics conditionally
    process_chars = {}
    for key in ['self_limiting_behavior', 'growth_per_cycle']:
        value = get_valid_param(process_characteristics, key)
        if value is not None:
            process_chars[key] = value

    # Create an instance of the template with the extracted data
    instance = template.comprehensive_ald_profile(
        label=f"Contribution {contribution_id}",
        process_parameter=template.ald_process_parameters(**process_params),
        film_property=template.ald_film_properties(**film_props),
        process_characteristic=template.ald_process_characteristics(**process_chars)
    )
    
    return instance, additional_reactants

def append_record_to_csv(record, additional_reactants, output_file_path):
    # If additional reactants exist, convert them to a string
    if additional_reactants:
        record['unused_reactants'] = ', '.join([str(reactant) for reactant in additional_reactants])
    
    # Check if the file exists, and create it if not
    if not os.path.exists(output_file_path):
        # Create the file with a header if it does not exist
        pd.DataFrame([record]).to_csv(output_file_path, index=False)
    else:
        # Append the record to the existing file
        pd.DataFrame([record]).to_csv(output_file_path, mode='a', header=False, index=False)


def load_processed_indices(output_file_path):
    """Load processed indices from the existing output CSV. Assumes the output CSV has entries in the order they were processed."""
    try:
        existing_df = pd.read_csv(output_file_path)
        # Create a set of processed indices based on the assumption that each line in the output corresponds to a processed entry in the input
        processed_indices = set(range(1, len(existing_df) + 1))
    except FileNotFoundError:
        processed_indices = set()
    return processed_indices

def load_paper_contributions(output_file_path):
    """Load existing contributions from the output file to initialize the next contribution id for each paper."""
    paper_contributions = {}
    if os.path.exists(output_file_path):
        existing_df = pd.read_csv(output_file_path)
        # Directly use the last contribution id encountered for each paper id in the output file
        for _, row in existing_df.iterrows():
            paper_contributions[row['paper id']] = row['contribution id']
    return paper_contributions


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
    processed_indices = load_processed_indices(output_file_path)
    paper_contributions = load_paper_contributions(output_file_path)
    
    # Track contributions per paper
    paper_contributions = {}
    
    ask_for_confirmation = True

    for index, row in data.iterrows():
        if index + 1 in processed_indices:
            print(f"skipped {row}")
            continue  # Skip this row as it has already been processed

        paper_id = row['paper_id']
        print(paper_id)
        if paper_id not in paper_contributions:
            paper_contributions[paper_id] = 0

        contribution_id = paper_contributions[paper_id] + 1
        paper_contributions[paper_id] = contribution_id

        extracted_info = json.loads(row['extracted_info'])

        # Ask user for confirmation only if the flag is True
        if ask_for_confirmation:
            confirmation = input(f"Do you want to save Contribution {contribution_id} for Paper ID {paper_id}? (yes/no/all): ").strip().lower()

            if confirmation in ['no', 'n']:
                print("Exiting workflow as requested.")
                return  # Exit the entire workflow
            elif confirmation == 'all':
                print("Automatically saving all remaining contributions.")
                ask_for_confirmation = False  # Set the flag to False to stop asking for confirmation
            elif confirmation not in ['yes', 'y', 'all']:
                print(f"Skipping Contribution {contribution_id} for Paper ID {paper_id}.")
                continue

        # Create and process the contribution if confirmation was 'yes', 'all', or not needed
        contribution, additional_reactants = create_contribution(extracted_info, contribution_id, template, reactant_mapping, material_mapping)

        # Prepare paper data and add to ORKG
        paper_data = {
            "predicates": [],
            "paper": {               
                "title": row['paper_title'],
                "researchField": "R254",
                "contributions": [contribution.template_dict['resource']]
                #"contributions": contribution_resource_id
            }
        }
        
        paper_response = orkg.papers.add(params=paper_data, merge_if_exists=True)
        print(f"paper response {paper_response.content}")
        
        # Logging information for paper addition
        print(f"Contribution added to Paper ID {paper_id}. Paper Response: {paper_response.content}")

        # Process response and append record to CSV file
        record = {
            "process_id": row.get('process_id', ''),
            "process_material": row.get('process_material', ''),  # Assuming this comes from the 'material' column
            "process_reactanta": row.get('process_reactanta', ''),
            "process_reactantb": row.get('process_reactantb', ''),
            "process_reactantc": row.get('process_reactantc', ''),
            "process_reactantd": row.get('process_reactantd', ''),
            "reference_doi": row.get('reference_doi', ''),             
            "contribution id": contribution_id,
            "paper title": row['paper_title'],
            "paper id": paper_id,  # Using paper_id directly from the input file
            #"contribution resource id": contribution_resource_id  # Contribution resource ID from the response
        }
        
        append_record_to_csv(record, additional_reactants, output_file_path)

        # Log the processed index
        processed_indices.add(index + 1)        
        
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
