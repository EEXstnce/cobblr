import requests
from clean.dbr import dbr_policy, dbr_price


def dbr_issue(api_endpoints):
  url = api_endpoints["dbr_policy"]
  response = requests.get(url)
  data = response.json(strict=False)
  policy = dbr_policy(data)
  pol = policy['dbr_policy']
  print(pol)

  url = api_endpoints["dbr_price"]
  response = requests.get(url)
  data = response.json(strict=False)
  price = dbr_price(data)
  pr = price['dbr_price']
  print(pr)

  issued = pol * pr
  return {"dbr_issue": issued}

