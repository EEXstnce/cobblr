from getters.inv_api import fetch

from util.printer import print_state
from util.asset import market_extractor, fixed_extractor, merge_data, merge_positions, clean_data
from util.firm import get_deposits_and_debt

from policy.pces import extract
from policy.dbr_issue import separate_datasets, get_newest_data


ma = "https://www.inverse.finance/api/f2/tvl"
#markets = fetch(ma, "data/state/markets.json")

fe = "https://www.inverse.finance/api/transparency/fed-overview"
#fed = fetch(fe, "data/state/fed.json")

fi = "https://www.inverse.finance/api/f2/fixed-markets"
#fixed = fetch(fi, "data/state/fixed.json")

po = "https://www.inverse.finance/api/f2/firm-positions"
#positions = fetch(po, "data/firm/positions.json")

d = "https://www.inverse.finance/api/transparency/dbr-emissions"
dbr = fetch(d, "data/state/dbr_issue.json")
a, b = separate_datasets(dbr)
dbr_policy = get_newest_data(b)
print(dbr_policy)


'''
market_ext = market_extractor("data/state/markets.json")
fixed_ext = fixed_extractor("data/state/fixed.json")
merge_point = 'name'
asset_merged = merge_data(market_ext, fixed_ext, merge_point)


deposits_and_debt = get_deposits_and_debt("data/firm/positions.json")
pces = extract(asset_merged)
merge = merge_positions(deposits_and_debt,pces)
clean = clean_data(merge)

firm_inv = clean_data(merge,"INV")
inv_stake = firm_inv[5]['deposits']

print(inv_stake)
'''