import requests
import json


def positions(data):
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
  output = {
    'positions': asset_data
  }
  return (output)
