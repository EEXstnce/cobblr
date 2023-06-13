from clean.debt_hist import debt_histo

def debt_time():
  debt = debt_histo()

  sec_yr = 365 * 24 * 60 * 60

  # Extract count_second and sum_debt values as a set, and divide count_second by sec_yr
  data_set = {((entry["count_second"] / sec_yr) * entry["sum_debt"]) for entry in debt}

  # Get the sum of entries in data_set
  total = sum(data_set)

  return {"burnt_dbr": total}
