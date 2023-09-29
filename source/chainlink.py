from script.util import getData


def raw(url, keys, config):
  # uses cryptocompare api
  data = getData(url)
  top = data[config[0]]
  key1 = top[keys[0]]
  key2 = key1[keys[1]]
  
  return {
    "last": key2[config[1]],
    "price": key2[config[2]],
    "vol": key2[config[3]],
    "high": key2[config[4]],
    "low": key2[config[5]]
  }