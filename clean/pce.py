import requests
import json


def tvl(data):
  # Extract asset names and TVLs
  asset_data = {}
  for item in data['firmTvls']:
    asset_data[item['market']['name']] = {'tvl': item['tvl']}

  # Format output
  # output = json.dumps(asset_data, indent=2, sort_keys=True)
  # print(output)

  return asset_data


def firm(data):
  # Extract asset names and TVLs
  asset_data = {}
  for item in data['markets']:
    asset_data[item['name']] = {
      'price': item['price'],
      'totalDebt': item['totalDebt'],
      'collateralFactor': item['collateralFactor'],
      'dolaLiquidity': item['dolaLiquidity'],
      'supplyApy': item['supplyApy'],
      'supplyApyLow': item['supplyApyLow'],
      'borrowPaused': item['borrowPaused']
    }

  # Format output
  # output = json.dumps(asset_data, indent=2, sort_keys=True)

  return asset_data


def combine(tvl_data, firm_data):
  # Extract asset names and TVLs
  asset_data = {}
  for item in tvl_data['firmTvls']:
    asset_data[item['market']['name']] = {'tvl': item['tvl']}
  for item in firm_data['markets']:
    asset_data[item['name']]['price'] = item['price']
    asset_data[item['name']]['totalDebt'] = item['totalDebt']
    asset_data[item['name']]['collateralFactor'] = item['collateralFactor']
    asset_data[item['name']]['dolaLiquidity'] = item['dolaLiquidity']
    asset_data[item['name']]['supplyApy'] = item['supplyApy']
    asset_data[item['name']]['supplyApyLow'] = item['supplyApyLow']
    asset_data[item['name']]['borrowPaused'] = item['borrowPaused']
  # Format output
  # output = json.dumps(asset_data, indent=2, sort_keys=True)
  return asset_data
