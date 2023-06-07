from clean.dbr import dbr_policy, dbr_price


def dbr_issue():
  policy = dbr_policy()
  pol = policy['dbr_policy']

  price = dbr_price()
  pr = price['dbr_price']

  issued = pol * pr
  return {"dbr_issue": issued}
