from getters.inv_api import fetch
from util.printer import print_info
from util.asset import market_extractor, fixed_extractor, merge_data, merge_positions, clean_data
from util.firm import get_deposits_and_debt, get_inv_deposits, filter_threshold
from policy.pces import extract
from policy.dbr_issue import separate_datasets, get_newest_data, dbr_price


# Define API endpoints
api_endpoints = {
    "markets": "https://www.inverse.finance/api/f2/tvl",
    "fed": "https://www.inverse.finance/api/transparency/fed-overview",
    "fixed": "https://www.inverse.finance/api/f2/fixed-markets",
    "positions": "https://www.inverse.finance/api/f2/firm-positions",
    "price": "https://www.inverse.finance/api/dbr",
    "dbr": "https://www.inverse.finance/api/transparency/dbr-emissions"
}

# Fetch data
data_files = {
    "markets": fetch(api_endpoints["markets"], "data/state/markets.json"),
    "fed": fetch(api_endpoints["fed"], "data/state/fed.json"),
    "fixed": fetch(api_endpoints["fixed"], "data/state/fixed-markets.json"),
    "positions": fetch(api_endpoints["positions"], "data/firm/positions.json"),
    "price": fetch(api_endpoints["price"], "data/state/dbr_fx.json"),
    "dbr": fetch(api_endpoints["dbr"], "data/state/dbr_issue.json")
}

# Calculate and print DBR FX
dbr_fx = dbr_price(data_files["price"])
print_info("DBR Fx", dbr_fx, "${:.5f}")

# Calculate and print DBR issuance per year
dbr_policy = separate_datasets(data_files["dbr"])
print_info("DBR Issuance per Year", dbr_policy, "{:,.0f}")

# Calculate and print DBR value per year
dbr_dola = dbr_policy * dbr_fx
print_info("DBR value per year", dbr_dola, "${:,.2f}")

# Extract and merge market data
market_ext = market_extractor("data/state/markets.json")
fixed_ext = fixed_extractor("data/state/fixed-markets.json")
asset_merged = merge_data(market_ext, fixed_ext, merge_point='name')

# Get deposits and debt
deposits_and_debt = get_deposits_and_debt("data/firm/positions.json")

# Extract pces data
pces = extract(asset_merged)

# Merge positions
merge = merge_positions(deposits_and_debt, pces)

# Clean merged data
clean = clean_data(merge)

# Calculate INV stake
firm_inv = clean_data(merge, "INV")
inv_stake = firm_inv[5]['deposits']
print_info("INV Staked", inv_stake, "{:,.2f}")

# Calculate DBR per INV
dbr_per_inv = dbr_policy / inv_stake
print_info("DBR / INV", dbr_per_inv, "{:.2f}")

# Calculate DBR value per INV
dbr_dola_inv = dbr_per_inv * dbr_fx
print_info("DBR value per INV", dbr_dola_inv, "${:,.2f}")

# Get INV deposits and filter based on threshold
inv_deposits = get_inv_deposits("data/firm/positions.json", dbr_per_inv, dbr_fx)
threshold = 1000
filtered = filter_threshold(inv_deposits, threshold)

#print(filtered)
