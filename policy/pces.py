import requests
import json

def extract(data):
    """
    Extract specific information from the input data.

    Args:
        data (list): The input data list.

    Returns:
        list: The extracted data list.
    """
    extracted_data = []
    for item in data:
        index = item['index']
        name = item['name']
        collateral_factor = item['collateralFactor']
        extracted_data.append({'index': index, 'name': name, 'collateralFactor': collateral_factor})

    # Write the data to the JSON file
    with open("data/policy/pce.json", "w") as file:
        json.dump(extracted_data, file)
      
    return extracted_data
