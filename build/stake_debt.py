from build.dbr_inv import dbr_per_inv
from clean.positions import positions


def stake_debt():
  d = dbr_per_inv()
  dbr = d["dbr_per_inv"]

  data = positions()

  position = [
    p for p in data['positions'] if p['marketIndex'] == 5 or p['debt'] > 0
  ]
  inv = [p for p in position if p["marketIndex"] == 5]

  for p in inv:
    p["dbr_earn"] = p["deposits"] * dbr
  inv_earn = [{"user": p["user"], "dbr_earn": p["dbr_earn"]} for p in inv]

  debt = [p for p in position if p["debt"] > 0]
  debt_user = [{"user": p["user"], "debt": p["debt"]} for p in debt]

  debt_earners = []
  for user in debt_user:
    for i in inv_earn:
      if user["user"] == i["user"]:
        user["dbr_earn"] = i["dbr_earn"]
        debt_earners.append(user)
        break

  total_earn = 0
  total_debt = 0
  for i in debt_earners:
    total_earn += i["dbr_earn"]
    total_debt -= i["debt"]

  return {"earn": total_earn, "burn": total_debt}
