from script.util import getData

last, price, vol, high, low = "LASTUPDATE", "PRICE", "VOLUME24HOUR", "HIGHDAY", "LOWDAY"


def raw(url, keys):
  # uses cryptocompare api
  u = url
  data = getData(u)
  raw = data["RAW"]
  lusd = raw[keys[0]]
  usd = lusd[keys[1]]
  return {
    "last": usd[last],
    "price": usd[price],
    "vol": usd[vol],
    "high": usd[high],
    "low": usd[low]
  }


def stables():
  pass
