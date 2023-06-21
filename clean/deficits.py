import requests
from util import getData


def deficits():
  url = "https://www.inverse.finance/api/f2/dbr-deficits"
  data = getData(url)
  dbr_holders = data["activeDbrHolders"]

  return dbr_holders
