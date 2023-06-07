from build.tvl_firm import tvl_firm


def inv_fx():
  tvl_data = tvl_firm()

  return {"inv_fx": tvl_data["INV"]["price"]}
