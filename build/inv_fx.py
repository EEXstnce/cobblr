from build.tvl_firm import tvl_firm
from build.dbr_inv import dbr_per_inv


def inv_fx():
  tvl_data = tvl_firm()

  return {"inv_fx": tvl_data["INV"]["price"]}


def inv_mult():
  pr = inv_fx()
  price = pr["inv_fx"]
  dbr = dbr_per_inv()
  earn = dbr["dollars_per_inv"]
  pe = price / earn

  return {"inv_mult": pe}
