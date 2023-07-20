from util import getData


def dbr_policy():
  url = "https://www.inverse.finance/api/transparency/dbr-emissions"
  data = getData(url)
  rates = data["rewardRatesHistory"]["rates"]
  newest_rate = max(rates, key=lambda x: x["timestamp"])
  return {"dbr_policy": newest_rate["yearlyRewardRate"]}


def dbr_price():
  url = "https://www.inverse.finance/api/dbr"
  data = getData(url)
  p = data["price"]
  return {"dbr_price": p}


def dbr_emissions():
  url = "https://www.inverse.finance/api/transparency/dbr-emissions"
  data = getData(url)
  emit = data["totalEmissions"]

  # Find the element with the highest timestamp
  max_timestamp_element = max(emit, key=lambda x: x['timestamp'])
  max_element = max_timestamp_element["accEmissions"]

  return {"dbr_emit": max_element}


def emissions_hist():
  url = "https://www.inverse.finance/api/transparency/dbr-emissions"
  data = getData(url)
  rates = data["rewardRatesHistory"]["rates"]

  return rates


def dbr_claim():
  url = "https://www.inverse.finance/api/transparency/dbr-emissions"
  data = getData(url)
  claimed = data["totalEmissions"]

  return claimed
