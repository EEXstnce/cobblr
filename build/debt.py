from clean.positions import positions


def debt():
  pos = positions()
  p = pos["positions"]
  total_debt = 0
  for item in p:
    total_debt += item["debt"]
  return {"debt": total_debt}