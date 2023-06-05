import requests


def inv_stake(api_endpoints):
  url = api_endpoints["positions"]
  response = requests.get(url)
  data = response.json()
  # Filter positions by marketIndex 5
  positions = [p for p in data['positions'] if p['marketIndex'] == 5]
  inv_staked = sum(p['deposits'] for p in positions)
  return {"inv_stake":inv_staked}
