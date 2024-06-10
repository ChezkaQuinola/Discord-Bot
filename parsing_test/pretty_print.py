import json
import pandas as pd

def json_to_spreadsheet(json_file, output_file):
    try:
        # Load JSON data from a file
        with open(json_file, 'r') as file:
            data = json.load(file)

        # Check if the JSON data is a list of dictionaries
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = pd.json_normalize(data)

        # Save the DataFrame to an Excel file
        df.to_excel(output_file, index=False, engine='openpyxl')

        print(f"Data successfully written to {output_file}")
    
    except FileNotFoundError:
        print(f"File {json_file} not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {json_file}.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
json_to_spreadsheet('data.json', 'output.xlsx')
