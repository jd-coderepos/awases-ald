import pandas as pd

def strip_doi_prefix(doi):
    # Remove the specified prefixes from the DOI
    prefixes = ["http://dx.doi.org/", "https://doi.org/"]
    for prefix in prefixes:
        if doi.startswith(prefix):
            return doi[len(prefix):]
    return doi

def transform_and_save_csv(input_file, output_file):
    # Load data from the input CSV file
    data = pd.read_csv(input_file, encoding='ISO-8859-1')  # Using 'ISO-8859-1' to avoid encoding issues

    # Select the required 'reference_doi' column, rename it, and clean up DOI prefixes
    new_data = data[['reference_doi']].copy()
    new_data['reference_doi'] = new_data['reference_doi'].apply(strip_doi_prefix)
    new_data.rename(columns={'reference_doi': 'paper:doi'}, inplace=True)

    # Add fixed values to the new columns
    new_data['paper:research_field'] = 'R254'
    new_data['contribution:research_problem'] = 'orkg:R676133'
    new_data['contribution:extraction_method'] = 'Automatic'

    # Drop duplicates based on 'paper:doi'
    new_data = new_data.drop_duplicates(subset=['paper:doi'])

    # Save the transformed data to the output CSV file
    new_data.to_csv(output_file, index=False)
    print(f"Data has been transformed and saved to {output_file}")

# Prompting user for the paths of the input and output CSV files
input_file_path = input("Enter the path of the input CSV file: ")
output_file_path = input("Enter the path of the output CSV file: ")

# Calling the function with user inputs
transform_and_save_csv(input_file_path, output_file_path)
