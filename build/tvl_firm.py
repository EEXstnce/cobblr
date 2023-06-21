from clean.pce import tvl_get, firm_get


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


def tvl_firm():
  tvl_data = tvl_get()
  firm_data = firm_get()

  # Combine TVL and firm data
  combined_data = combine(tvl_data, firm_data)
  return combined_data
