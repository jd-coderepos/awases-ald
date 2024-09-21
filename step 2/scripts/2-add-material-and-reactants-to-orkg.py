import pandas as pd
from orkg import ORKG
from getpass import getpass

def read_csv_with_encoding(file_path, encoding='utf-8'):
    try:
        return pd.read_csv(file_path, encoding=encoding)
    except UnicodeDecodeError:
        return pd.read_csv(file_path, encoding='ISO-8859-1')

def process_items(orkg, data, item_columns):
    items = data[item_columns].fillna('')
    items_list = set(items.values.flatten()) - {''}

    items_info = []

    for item in items_list:
        response_data = orkg.resources.find_or_add(label=item).content
        print(f"Response for {item}: {response_data}")  # Print the direct dictionary response

        if 'id' in response_data:
            items_info.append({
                'Name': item, 
                'ORKG Resource ID': response_data['id'], 
                'Status': 'Processed'
            })
            print(f"Successfully processed resource {item}, ID: {response_data['id']}")
        else:
            error_detail = response_data.get('message', 'Unknown error')
            items_info.append({
                'Name': item, 
                'Status': 'Failed', 
                'Detail': error_detail
            })
            print(f"Failed to process resource {item}: {error_detail}")

    return items_info

def main():
    host_address = input("Enter the ORKG host address: ")
    email = input("Enter your ORKG email address: ")
    password = getpass("Enter your ORKG password: ")
    input_file_path = input("Enter the path of the input CSV file: ")
    reactants_output_path = input("Enter the path of the reactants output CSV file: ")
    materials_output_path = input("Enter the path of the materials output CSV file: ")

    orkg = ORKG(host=host_address, creds=(email, password))
    data = read_csv_with_encoding(input_file_path)

    reactant_columns = ['process_reactanta', 'process_reactantb', 'process_reactantc', 'process_reactantd']
    reactants_info = process_items(orkg, data, reactant_columns)
    reactants_df = pd.DataFrame(reactants_info)
    reactants_df.to_csv(reactants_output_path, index=False)
    print(f"Reactants information has been written to {reactants_output_path}")

    material_columns = ['process_material']
    materials_info = process_items(orkg, data, material_columns)
    materials_df = pd.DataFrame(materials_info)
    materials_df.to_csv(materials_output_path, index=False)
    print(f"Materials information has been written to {materials_output_path}")

if __name__ == "__main__":
    main()
