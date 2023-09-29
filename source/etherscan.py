from script.util import getData

def scan(url, keys, config):
  # uses etherscan api
  data = getData(url)
  top = data[config[0]]

  return top

def scan2(url, keys, config, num_results=10):
  data = getData(url)  
  top = data[config[0]]

  # Initialize an empty dictionary
  results = {}

  # This loop will add the last 10 results to the `results` dictionary 
  for i in range(num_results):
    result = top[i]
    results[i] = result

  return results

