import pandas as pd
import os
from openai import OpenAI
import getpass
import json

def generate_unique_key(row):
    # Combine DOI with material and reactants to form a unique key
    reactants = [row['process_reactanta'], row['process_reactantb'], row['process_reactantc'], row['process_reactantd']]
    key_components = [row['reference_doi']] + [str(x) for x in reactants if pd.notna(x)]
    return '_'.join(key_components)

def load_processed_records(record_file_path):
    try:
        with open(record_file_path, 'r') as file:
            processed_keys = set(file.read().splitlines())
    except FileNotFoundError:
        processed_keys = set()
    return processed_keys

def update_processed_records(record_file_path, processed_keys):
    with open(record_file_path, 'w') as file:
        file.write('\n'.join(processed_keys))

def read_input_files(materials_path, reactants_path, papers_path, raw_data_path):
    # Similar as before, merge and map dataframes
    materials_df = pd.read_csv(materials_path)
    reactants_df = pd.read_csv(reactants_path)
    papers_df = pd.read_csv(papers_path)
    raw_data_df = pd.read_csv(raw_data_path)
    
    papers_df.rename(columns={'doi': 'reference_doi'}, inplace=True)
    combined_df = pd.merge(raw_data_df, papers_df, on='reference_doi', how='left')
    
    return materials_df, reactants_df, combined_df

def format_system_message(row):
    # Create a list of reactants, converting each to a string only if it's not NaN
    reactants = [
        str(row['process_reactanta']) if pd.notna(row['process_reactanta']) else None,
        str(row['process_reactantb']) if pd.notna(row['process_reactantb']) else None,
        str(row['process_reactantc']) if pd.notna(row['process_reactantc']) else None,
        str(row['process_reactantd']) if pd.notna(row['process_reactantd']) else None
    ]
    # Filter out any None entries, which represent empty cells
    reactants_list = ', '.join(filter(None, reactants))

    system_message = f'''
        <role>
            You are assigned as a specialist in Atomic Layer Deposition (ALD). Your primary task is to process scientific articles related to ALD, extracting specific scientific information as detailed below. The ALD process involves the material {row['process_material']} and reactants {reactants_list}. This context defines the scope of the extraction task and the information is prepopulated in the extraction schema.
        </role>

        <task>
            Upon receiving an article, identify and extract data according to a predefined schema. Record values for each property specified in the schema. If a property is not mentioned in the article, denote this with a "-". For properties discussed in the article that are not included in the schema, extract these as well and list them under an "extra_properties" section as key-value pairs.
        </task>

        <extraction-schema>
        [
            {{
                "process_parameters": {{
                    "reactants": [
                        "{reactants_list}"
                    ],
                    "temperature_range": "Range of temperatures used for the deposition process",
                    "pressure_range": "Range of pressures used for the deposition process"
                }},
                "film_properties": {{
                    "material": "{row['process_material']}",
                    "thickness_control": "Methods and results of thickness control",
                    "uniformity": "Uniformity of the film across the substrate",
                    "conformality": "Conformality of the film on 3D structures",
                    "film_thickness": "Thickness of the deposited film",
                    "film_density": "Density of the deposited film",
                    "surface_roughness": "Surface roughness of the deposited film",
                    "refractive_index": "Refractive index of the deposited film"
                }},
                "process_characteristics": {{
                    "self_limiting_behavior": "Evidence of self-limiting behavior in the ALD process",
                    "nucleation_behavior": "Description of nucleation behavior observed",
                    "growth_per_cycle": "Growth per cycle observed in the process"
                }},
                "safety": "Safety considerations for the process and materials",
                "stability": "Stability of the deposited films over time",
                "reproducibility": "Reproducibility of the film thickness and properties",
                "precursor_consumption": "Efficiency and consumption rate of precursors",
                "device_performance": "Performance of the ALD films in practical devices",
                "extra_properties": {{
                    "Additional property 1": "Value of additional property 1",
                    "Additional property 2": "Value of additional property 2",
                    "..."
                }}
            }}
        ]
        </extraction-schema>

        <output-response-format>
            Your responses should be formatted in JSON, strictly adhering to the provided schema. Ensure the formatting and data integrity are maintained as per the guidelines. Use the "-" symbol for any property not mentioned in the article.
        </output-response-format>
    '''
    return system_message

def extract_and_process(client, row):
    formatted_message = format_system_message(row)
    full_text = row['full_text']
    valid_json = False
    attempts = 0

    while not valid_json and attempts < 5:  # Limit retries to prevent infinite loops
        attempts += 1
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": formatted_message},
                {"role": "user", "content": f"Extract the information as instructed from this article:\n{full_text}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            seed=54,
        )
        
        # Check if the response is valid JSON
        try:
            # Attempt to parse the JSON to see if it's valid
            json.loads(completion.choices[0].message.content)
            valid_json = True  # Set flag to True if parsing is successful
        except json.JSONDecodeError:
            print(f"Invalid JSON received on attempt {attempts}. Retrying...")
            valid_json = False
        
        # Sleep briefly to avoid hitting the API too rapidly in a loop
        if not valid_json:
            import time
            time.sleep(1)

    # Return the last response received, valid or otherwise, to handle cases where valid JSON is never returned
    return completion.choices[0].message.content

def main():
    api_key = getpass.getpass('Enter your OpenAI API key: ')
    client = OpenAI(api_key=api_key)
    
    # Setup paths and load files
    materials_path = input("Enter the file path for materials CSV: ")
    reactants_path = input("Enter the file path for reactants CSV: ")
    papers_path = input("Enter the file path for papers CSV: ")
    raw_data_path = input("Enter the file path for raw data CSV: ")
    record_file_path = input("Enter the record file path (e.g., 'processed_records.txt'): ")
    
    _, _, combined_df = read_input_files(materials_path, reactants_path, papers_path, raw_data_path)
    processed_keys = load_processed_records(record_file_path)
    output_file_path = input("Enter the output file path (e.g., 'output_data.csv'): ")
    
    first_run = True
    
    for index, row in combined_df.iterrows():
        unique_key = generate_unique_key(row)
        if unique_key not in processed_keys:
            extracted_info = extract_and_process(client, row) if pd.notna(row['full_text']) else "-"
            combined_df.at[index, 'extracted_info'] = extracted_info
            
            # Write output and update records
            output_df = combined_df.loc[[index], ['process_id', 'process_material', 'process_reactanta', 'process_reactantb', 'process_reactantc', 'process_reactantd', 'reference_doi', 'paper_id', 'paper_title', 'extracted_info']]
            output_df.to_csv(output_file_path, mode='a', header=first_run, index=False)
            first_run = False
            processed_keys.add(unique_key)
            update_processed_records(record_file_path, processed_keys)
            
            if index == 0:
                print(f"First entry processed. Check the output in {output_file_path}. Continue with the rest? (yes/no):")
                if input().strip().lower() != 'yes':
                    break
        else:
            print(f"Skipping already processed entry for key: {unique_key}")

if __name__ == "__main__":
    main()
