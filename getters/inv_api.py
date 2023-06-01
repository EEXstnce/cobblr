import requests
import json
from datetime import datetime


def fetch(api_url, filename):
    # Send GET request to the API endpoint
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Add timestamp to the data
        data["timestamp"] = datetime.now().isoformat()

        # Write the data to the JSON file
        with open(filename, "w") as file:
            json.dump(data, file)

        return data
    else:
        return None
