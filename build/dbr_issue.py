from clean.dbr import dbr_policy, dbr_price
from build.debt import debt


def dbr_issue():
  policy = dbr_policy()
  pol = policy['dbr_policy']

  price = dbr_price()
  pr = price['dbr_price']

  issued = pol * pr
  return {"dbr_issue": issued}

def dbr_net():
  issue = dbr_policy()
  iss = issue['dbr_policy']
  
  dt = debt()
  d = dt["debt"]

  net = iss - d
  
  return {"dbr_net": net}