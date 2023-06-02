from flask import Flask, request, render_template, jsonify
from werkzeug.exceptions import HTTPException
import pickle

from getters.inv_api import fetch
from util.printer import print_info
from util.asset import market_extractor, fixed_extractor, merge_data, merge_positions, clean_data
from util.firm import get_deposits_and_debt, get_inv_deposits, filter_threshold
from policy.pces import extract
from policy.dbr_issue import separate_datasets, get_newest_data, dbr_price

app = Flask(__name__)
hits = 0
errors = 0


@app.route("/")
def index():
  global hits
  hits += 1
  return render_template("errors.html", e=str(e)), code


@app.route("/docs")
def docs():
  global hits
  hits += 1
  return render_template("docs.html")


@app.errorhandler(Exception)
def error(e):
  global errors
  errors += 1
  code = 500
  if isinstance(e, HTTPException):
    code = e.code
  return render_template("errors.html", e=str(e)), code


@app.route("/api", methods=["GET", "POST"])
def api():
  global hits, errors
  hits += 1

  data = request.args.get("data")
  token = request.args.get("token")
  with open("tokens.pkl", "rb") as t:
    if token is not None:
      if token in pickle.loads(t.read()):
        auth = True
      else:
        auth = False
    else:
      auth = False

  if data is None:
    return jsonify({"type": "Error", "content": "No data requested"})
  elif data == "hits":
    return jsonify({"type": "HitCount", "content": hits})
  elif data == "errors" and not auth:
    return jsonify({"type": "Error", "content": "Not authenticated"}), 401
  elif data == "errors" and auth:
    return jsonify({"type": "ErrorCount", "content": errors})
  else:
    return jsonify({
      "type": "Error",
      "content": "Data specified does not exist"
    })


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


@app.route('/data')
def get_data():
  global data_files
  if not data_files:
    for key, url in api_endpoints.items():
      data_files[key] = fetch(url, f"data/state/{key}.json")
  return jsonify(data_files)


@app.route('/dbr_fx')
def get_dbr_fx():
  try:
    dbr_fx = dbr_price(data_files["price"])
    return jsonify({"dbr_fx": dbr_fx})
  except Exception as e:
    return jsonify({"error": str(e)}), 500


@app.route('/dbr_issuance')
def get_dbr_issuance():
  dbr_policy = separate_datasets(data_files["dbr"])
  return jsonify({"dbr_issuance": dbr_policy})


@app.route('/dbr_value')
def get_dbr_value():
  dbr_fx = dbr_price(data_files["price"])
  dbr_policy = separate_datasets(data_files["dbr"])
  dbr_dola = dbr_policy * dbr_fx
  return jsonify({"dbr_value": dbr_dola})


@app.route('/inv_stake')
def get_inv_stake():
  market_ext = market_extractor("data/state/markets.json")
  fixed_ext = fixed_extractor("data/state/fixed-markets.json")
  asset_merged = merge_data(market_ext, fixed_ext, merge_point='name')
  deposits_and_debt = get_deposits_and_debt("data/firm/positions.json")
  pces = extract(asset_merged)
  merge = merge_positions(deposits_and_debt, pces)
  clean = clean_data(merge)
  firm_inv = clean_data(merge, "INV")
  inv_stake = firm_inv[5]['deposits']
  return jsonify({"inv_stake": inv_stake})


@app.route('/dbr_per_inv')
def get_dbr_per_inv():
  market_ext = market_extractor("data/state/markets.json")
  fixed_ext = fixed_extractor("data/state/fixed-markets.json")
  asset_merged = merge_data(market_ext, fixed_ext, merge_point='name')
  deposits_and_debt = get_deposits_and_debt("data/firm/positions.json")
  pces = extract(asset_merged)
  merge = merge_positions(deposits_and_debt, pces)
  clean = clean_data(merge)
  firm_inv = clean_data(merge, "INV")
  inv_stake = firm_inv[5]['deposits']
  dbr_policy = separate_datasets(data_files["dbr"])
  dbr_per_inv = dbr_policy / inv_stake
  return jsonify({"dbr_per_inv": dbr_per_inv})


@app.route('/dbr_value_per_inv')
def get_dbr_value_per_inv():
  market_ext = market_extractor("data/state/markets.json")
  fixed_ext = fixed_extractor("data/state/fixed-markets.json")
  asset_merged = merge_data(market_ext, fixed_ext, merge_point='name')
  deposits_and_debt = get_deposits_and_debt("data/firm/positions.json")
  pces = extract(asset_merged)
  merge = merge_positions(deposits_and_debt, pces)
  clean = clean_data(merge)
  firm_inv = clean_data(merge, "INV")
  inv_stake = firm_inv[5]['deposits']
  dbr_policy = separate_datasets(data_files["dbr"])
  dbr_fx = dbr_price(data_files["price"])
  dbr_per_inv = dbr_policy / inv_stake
  dbr_dola_inv = dbr_per_inv * dbr_fx
  return jsonify({"dbr_value_per_inv": dbr_dola_inv})


@app.route('/filtered_inv_deposits')
def get_filtered_inv_deposits():
  market_ext = market_extractor("data/state/markets.json")
  fixed_ext = fixed_extractor("data/state/fixed-markets.json")
  asset_merged = merge_data(market_ext, fixed_ext, merge_point='name')
  deposits_and_debt = get_deposits_and_debt("data/firm/positions.json")
  pces = extract(asset_merged)
  merge = merge_positions(deposits_and_debt, pces)
  clean = clean_data(merge)
  firm_inv = clean_data(merge, "INV")
  inv_stake = firm_inv[5]['deposits']
  dbr_policy = separate_datasets(data_files["dbr"])
  dbr_fx = dbr_price(data_files["price"])
  dbr_per_inv = dbr_policy / inv_stake
  inv_deposits = get_inv_deposits("data/firm/positions.json", dbr_per_inv,
                                  dbr_fx)
  threshold = 1000
  filtered = filter_threshold(inv_deposits, threshold)
  return jsonify({"filtered_inv_deposits": filtered})


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000)
