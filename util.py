import os
import json
import time
import requests


def getData(url_in):
  url = url_in
  response = requests.get(url)
  data = response.json()
  return data


def format_output(output):
  return json.dumps(json.loads(output), indent=2)


def printToJson(obj, fileName):
  if not os.path.exists('data/' + fileName + '.json'):
    open('data/' + fileName + '.json', 'w').close()

  with open('data/' + fileName + '.json', 'a') as outfile:
    outfile.write('{' + '"timestamp":' + time.strftime("%d/%m/%Y %H:%M:%S") +
                  ',')
    outfile.write(format_output(json.dumps(obj)) + '},')
