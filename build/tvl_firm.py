import requests
from clean.pce import combine


def tvl_firm(api_endpoints):
  # Get TVL data from API endpoint
  tvl_url = api_endpoints["tvl"]
  tvl_response = requests.get(tvl_url)
  tvl_data = tvl_response.json()

  # Get firm data from API endpoint
  firm_url = api_endpoints["firm"]
  firm_response = requests.get(firm_url)
  firm_data = firm_response.json()

  # Combine TVL and firm data
  combined_data = combine(tvl_data, firm_data)
  return combined_data
