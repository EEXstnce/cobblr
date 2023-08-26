from script.util import getData


def raw(url, keys, config):
  # uses cryptocompare api
  u = url
  data = getData(u)
  raw = data["RAW"]
  lusd = raw[keys[0]]
  usd = lusd[keys[1]]
  return {
    "last": usd[config[0]],
    "price": usd[config[1]],
    "vol": usd[config[2]],
    "high": usd[config[3]],
    "low": usd[config[4]]
  }