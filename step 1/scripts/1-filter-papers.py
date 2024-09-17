import pandas as pd

def filter_and_save_csv_data(input_file, output_file):
    try:
        # Attempt to load the data from the CSV file with a more permissive encoding
        data = pd.read_csv(input_file, encoding='ISO-8859-1')
    except UnicodeDecodeError as e:
        print(f"Failed to read the file due to an encoding issue: {e}")
        return
    
    # Filter the data to exclude rows where 'full_text' is a dash ('-')
    filtered_data = data[data['full_text'] != '-']
    
    # Save the filtered data to a CSV file
    filtered_data.to_csv(output_file, index=False)
    print(f"Filtered data saved to {output_file}")

# Prompting user to input the paths for the input and output files
input_file_path = input("Enter the path of the input CSV file: ")
output_file_path = input("Enter the path of the output CSV file: ")

# Calling the function with user inputs
filter_and_save_csv_data(input_file_path, output_file_path)
