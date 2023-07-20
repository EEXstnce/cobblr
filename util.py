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


def printToJson(obj, fileName):
  """
  Write the given object to a JSON file with the specified file name.

  Parameters:
  obj: The object to write to the JSON file.
  fileName (str): The name of the JSON file to write to.
  """
  if not os.path.exists('data/' + fileName + '.json'):
    open('data/' + fileName + '.json', 'w').close()

  with open('data/' + fileName + '.json', 'a') as outfile:
    outfile.write('{' + '"timestamp":' + time.strftime("%d/%m/%Y %H:%M:%S") +
                  ',')
    outfile.write
