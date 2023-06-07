import requests


def dbr_policy():
  url = "https://www.inverse.finance/api/transparency/dbr-emissions"
  response = requests.get(url)
  data = response.json()
  rates = data["rewardRatesHistory"]["rates"]
  newest_rate = max(rates, key=lambda x: x["timestamp"])
  return {"dbr_policy": newest_rate["yearlyRewardRate"]}


def dbr_price():
  url = "https://www.inverse.finance/api/dbr"
  response = requests.get(url)
  data = response.json()
  p = data["price"]
  return {"dbr_price": p}
