from script.util import getData


def scan(url, keys, config):
  # uses etherscan api
  data = getData(url)
  top = data[config[0]]

  return top
