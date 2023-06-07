from clean.dbr import dbr_policy
from build.dbr_issue import dbr_issue
from build.inv_stake import inv_stake


def dbr_per_inv():
  inv_staked = inv_stake()
  staked = inv_staked['inv_stake']

  dbr_pol = dbr_policy()
  policy = dbr_pol['dbr_policy']

  dbr_iss = dbr_issue()
  issue = dbr_iss['dbr_issue']

  dbr_inv = policy / staked
  dol_inv = issue / staked

  return {"dbr_per_inv": dbr_inv, "dollars_per_inv": dol_inv}
