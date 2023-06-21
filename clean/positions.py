from util import getData


def positions():
  url = "https://www.inverse.finance/api/f2/firm-positions"
  data = getData(url)
  # Extract asset names and TVLs
  asset_data = []
  for item in data['positions']:
    asset_data.append({
      'marketIndex': item['marketIndex'],
      'user': item['user'],
      'liquidatableDebt': item['liquidatableDebt'],
      'deposits': item['deposits'],
      'debt': item['debt']
    })

  # Format output
  output = {'positions': asset_data}
  return (output)
