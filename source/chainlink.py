from script.util import getData


def raw(url):
  u = url
  data = getData(u)
  raw = data["RAW"]
  lusd = raw["LUSD"]
  usd = lusd["USD"]
  return {
    "last": usd["LASTUPDATE"],
    "price": usd["PRICE"],
    "vol": usd["VOLUME24HOUR"],
    "high": usd["HIGHDAY"],
    "low": usd["LOWDAY"]
  }
