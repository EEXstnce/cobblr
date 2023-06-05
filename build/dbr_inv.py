import requests
from clean.dbr import dbr_policy
from build.inv_stake import inv_stake


def dbr_per_inv(api_endpoints):
  url = api_endpoints["dbr_policy"]
  response = requests.get(url)
  data = response.json()
  dbr_pol = dbr_policy(data)

  inv_staked = inv_stake(api_endpoints)

  dbr_per_inv = dbr_pol / inv_staked
  return dbr_per_inv
