from util import getData

from clean.dbr import dbr_claim

apikey = "3ZPZ7M8X6D132TYZ84MD4KTIC621AG1XAY"


def hash_address(i):
  url = f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionReceipt&txhash={i}&apikey={apikey}"
  data = getData(url)

  if "result" in data and "from" in data["result"]:
    addr = data["result"]["from"]
    return addr


def dbr_swaps():
  claims = dbr_claim()
  addr_list = [hash_address(claim['txHash']) for claim in claims]

  DBR = "0xAD038Eb671c44b853887A7E32528FaB35dC5D710"
  INV = "0x41D5D79431A913C4aE7d69a668ecdfE5fF9DFB68"

  matching_hashes = []  # Renamed 'list' variable
  total_value = 0

  for addr in addr_list:
    dbr_url = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={DBR}&address={addr}&page=1&offset=5000&startblock=0&endblock=999999999&sort=desc&apikey=3ZPZ7M8X6D132TYZ84MD4KTIC621AG1XAY"
    inv_url = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={INV}&address={addr}&page=1&offset=5000&startblock=0&endblock=999999999&sort=desc&apikey=3ZPZ7M8X6D132TYZ84MD4KTIC621AG1XAY"

    dbr_data = getData(dbr_url)

    dbr_result = dbr_data["result"]
    hash_list = [item["hash"] for item in dbr_result]

    inv_data = getData(inv_url)

    inv_result = inv_data["result"]
    inv_list = [item["hash"] for item in inv_result]

    for item in inv_list:
      if item in hash_list:
        matching_hashes.append(item)

    inv_tx = []
    for item in inv_result:
      if item["hash"] in matching_hashes:
        if "value" in item:  # Check if "value" field exists
          total_value += int(item["value"])
        inv_tx.append(item)

  print("Total Value:", total_value / 10**18)  # Print the calculated total value

  return {"total_value": total_value}
