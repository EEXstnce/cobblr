from build.dbr_float import filter_stakers
from clean.deficits import deficits


def loans():

  week_iss = filter_stakers()
  week_iss = week_iss["w"]

  dbr_holders = deficits()

  bal_debt = [{
    "bal": p["signedBalance"],
    "debt": p["debt"]
  } for p in dbr_holders]

  bal_debt = [p for p in bal_debt if p["debt"] > 0]

  for p in bal_debt:
    p["daily_spend"] = p["debt"] / 365

  bal_spend = [{
    "bal": p["bal"],
    "day_spend": p["daily_spend"],
    "depl_days": (p["bal"] / p["daily_spend"])
  } for p in bal_debt]

  day_spend = sum(p["day_spend"] for p in bal_spend)
  week_spend = day_spend * 7

  week_net = week_iss - week_spend

  return {
    "week_spend": week_spend,
    "week_net": week_net,
    "bal_spend": bal_spend
  }
