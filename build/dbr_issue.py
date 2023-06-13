from clean.dbr import dbr_policy, dbr_price, emissions_hist, dbr_emissions
from build.debt import debt

import time


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


def dbr_avail():
  current_timestamp = time.time()

  emissions = emissions_hist()
  seconds_in_year = 365 * 24 * 60 * 60  # Number of seconds in a year

  total_result = 0

  for i in range(len(emissions)):
    if i == len(emissions) - 1:
      emissions[i]['timeDifference'] = (
        current_timestamp -
        (emissions[i]['timestamp'] / 1000)) / seconds_in_year
    else:
      emissions[i]['timeDifference'] = (
        (emissions[i + 1]['timestamp'] / 1000) -
        (emissions[i]['timestamp'] / 1000)) / seconds_in_year

    emissions[i]['result'] = emissions[i]['timeDifference'] * emissions[i][
      'yearlyRewardRate']
    total_result += emissions[i]['result']

  return {"dbr_avail": total_result}


def dbr_accrued():
  emit = dbr_emissions()
  e = emit["dbr_emit"]

  avail = dbr_avail()
  a = avail["dbr_avail"]

  accrued = a - e

  return {"accrued_dbr": accrued}
