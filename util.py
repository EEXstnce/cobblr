import os
import json
import time
import requests


def getData(url_in):
  """
    Send a GET request to the specified URL and return the response as JSON data.

    Parameters:
    url_in (str): The URL to send the GET request to.

    Returns:
    dict: The JSON data response from the URL.
    """
  url = url_in
  response = requests.get(url)
  data = response.json()
  return data


def format_output(output):
  """
    Format the output by converting it to a nicely indented JSON string.

    Parameters:
    output (str): The output to format.

    Returns:
    str: The formatted JSON string.
    """
  return json.dumps(json.loads(output), indent=2)


def isDataInFile(data_str, fileName):
  """
    Check if the given data as a string exists in the JSON file.

    Parameters:
    data_str (str): The JSON data as a string to check.
    fileName (str): The name of the JSON file to search in.

    Returns:
    bool: True if the data exists in the file, False otherwise.
    """
  file_path = 'data/' + fileName + '.json'
  if not os.path.exists(file_path):
    return False

  with open(file_path, 'r') as infile:
    for line in infile:
      try:
        data = json.loads(line)
        if data['data'] == data_str:
          return True
      except json.JSONDecodeError:
        continue

  return False


def printToJson(data_str, fileName):
  """
    Append the given data as a string to a JSON file with the specified file name,
    but only if it doesn't already exist in the file.

    Parameters:
    data_str (str): The JSON data as a string to append to the JSON file.
    fileName (str): The name of the JSON file to append to.
    """
  if not isDataInFile(data_str, fileName):
    file_path = 'data/' + fileName + '.json'
    with open(file_path, 'a') as outfile:
      timestamp = time.strftime("%d/%m/%Y %H:%M:%S")
      data = {'timestamp': timestamp, 'data': data_str}
      json.dump(data, outfile)
      outfile.write('\n')  # Add a newline to separate multiple JSON objects
