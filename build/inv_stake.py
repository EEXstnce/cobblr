from clean.positions import positions


def inv_stake():
  data = positions()
  # Filter positions by marketIndex 5
  position = [p for p in data['positions'] if p['marketIndex'] == 5]
  inv_staked = sum(p['deposits'] for p in position)
  return {"inv_stake": inv_staked}
