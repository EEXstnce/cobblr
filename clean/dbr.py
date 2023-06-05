def dbr_policy(data):
  # Splitting the data into two datasets
  if "rewardRatesHistory" in data:
    rates = data["rewardRatesHistory"]["rates"]
    newest_rate = max(rates, key=lambda x: x["timestamp"])
    return {"dbr_policy": newest_rate["yearlyRewardRate"]}


def dbr_price(data):

  p = data["price"]
  return {"dbr_price": p}
