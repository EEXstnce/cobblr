from build.dbr_inv import dbr_per_inv
from clean.dbr import dbr_price
from build.stake_debt import stake_debt
from clean.positions import positions


def filter_stakers():
  dbr_per = dbr_per_inv()
  dbr = dbr_per["dollars_per_inv"]

  db = dbr_price()
  dbr_cost = db["dbr_price"]

  deb = stake_debt()
  de = deb["burn"]

  data = positions()
  position = [p for p in data['positions'] if p['marketIndex'] == 5]

  deposits = [p['deposits'] for p in position]
  deposits = sorted(deposits)

  costs = 45

  year = [d * dbr for d in deposits]
  year = [y if y > 4 * costs else 0 for y in year]
  year_sum = (sum(year) / dbr_cost) + de

  quarter = [y / 4 for y in year]
  quarter = [q if q > 4 * costs else 0 for q in quarter]
  quarter_sum = (sum(quarter) / dbr_cost) + (de / 4)

  month = [y / 12 for y in year]
  month = [m if m > 4 * costs else 0 for m in month]
  month_sum = (sum(month) / dbr_cost) + (de / 12)

  week = [y / 52 for y in year]
  week = [w if w > 4 * costs else 0 for w in week]
  week_sum = (sum(week) / dbr_cost) + (de / 52)

  return {"y": year_sum, "q": quarter_sum, "m": month_sum, "w": week_sum}
