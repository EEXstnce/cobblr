import requests
import os
from flask import Flask, request, render_template, jsonify
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from flask_caching import Cache

from clean.dbr import dbr_policy, dbr_price
from clean.pce import tvl, firm, combine
from clean.positions import positions

from build.tvl_firm import tvl_firm
from build.dbr_issue import dbr_issue
from build.inv_stake import inv_stake
from build.dbr_inv import dbr_per_inv
from build.inv_fx import inv_fx, inv_mult
from build.debt import debt

from util import printToJson

app = Flask(__name__)
CORS(app)
cache = Cache(app,
              config={
                'CACHE_TYPE': 'filesystem',
                'CACHE_DIR': 'data/cache'
              })
hits = 0
errors = 0

# Define API endpoints
api_endpoints = {
  "tvl": "https://www.inverse.finance/api/f2/tvl",
  "firm": "https://www.inverse.finance/api/f2/fixed-markets",
  "positions": "https://www.inverse.finance/api/f2/firm-positions",
  "dbr_price": "https://www.inverse.finance/api/dbr",
  "dbr_policy": "https://www.inverse.finance/api/transparency/dbr-emissions"
}

# Define endpoint function mappings
endpoint_functions = {
  "tvl_firm": tvl_firm,
  "dbr_issue": dbr_issue,
  "inv_stake": inv_stake,
  "dbr_inv": dbr_per_inv
}


@app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def catch_all_options(path):
  return '', 200


@app.route("/")
def index():
  global hits
  hits += 1
  print("Route '/' hit")
  return render_template("index.html")


@app.route("/docs")
def docs():
  global hits
  hits += 1
  print("Route '/docs' hit")
  return render_template("docs.html")


@app.errorhandler(Exception)
def error(e):
  global errors
  errors += 1
  code = 500
  if isinstance(e, HTTPException):
    code = e.code
  print(f"Error: {str(e)}")
  return render_template("errors.html", e=str(e)), code


@app.route("/api", methods=["GET", "POST"])
def api():
  global hits, errors
  hits += 1
  print("Route '/api' hit")

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
    print("No data requested")
    return jsonify({"type": "Error", "content": "No data requested"})
  elif data == "hits":
    print("Data requested: hits")
    return jsonify({"type": "HitCount", "content": hits})
  elif data == "errors" and not auth:
    print("Data requested: errors (not authenticated)")
    return jsonify({"type": "Error", "content": "Not authenticated"}), 401
  elif data == "errors" and auth:
    print("Data requested: errors")
    return jsonify({"type": "ErrorCount", "content": errors})
  else:
    print("Invalid data specified")
    return jsonify({
      "type": "Error",
      "content": "Data specified does not exist"
    })


def endpoint(func, name):
  global hits, errors
  hits += 1
  try:
    data = func()
    printToJson(data, name)
    cache.set(name, data, timeout=5 * 60)  # Cache data for 5 minutes
    return data
  except:
    errors += 1
    cached_data = cache.get(name)  # Get cached data if it exists
    if cached_data is not None:
      return cached_data
    return jsonify({
      "success": False,
      "message": f"Error fetching {name} data"
    }), 500


@app.route("/dbr_policy", methods=["GET"])
def dbr_policy_endpoint():
  return endpoint(dbr_policy, "dbr_policy")


@app.route("/dbr_price", methods=["GET"])
def dbr_price_endpoint():
  return endpoint(dbr_price, "dbr_price")


@app.route("/tvl", methods=["GET"])
def tvl_endpoint():
  return endpoint(tvl, "tvl")


@app.route("/firm", methods=["GET"])
def firm_endpoint():
  return endpoint(firm, "firm")


@app.route("/positions", methods=["GET"])
def positions_endpoint():
  return endpoint(positions, "positions")


@app.route("/debt", methods=["GET"])
def debt_endpoint():
  return endpoint(debt, "debt")


@app.route("/tvl_firm", methods=["GET"])
def tvl_firm_endpoint():
  return endpoint(tvl_firm, "tvl_firm")


@app.route("/dbr_issue", methods=["GET"])
def dbr_issue_endpoint():
  return endpoint(dbr_issue, "dbr_issue")


@app.route("/inv_stake", methods=["GET"])
def inv_stake_endpoint():
  return endpoint(inv_stake, "inv_stake")


@app.route("/dbr_inv", methods=["GET"])
def dbr_inv_endpoint():
  return endpoint(dbr_per_inv, "dbr_inv")


@app.route("/inv_fx", methods=["GET"])
def inv_fx_endpoint():
  return endpoint(inv_fx, "inv_fx")


@app.route("/inv_mult", methods=["GET"])
def inv_mult_endpoint():
  return endpoint(inv_mult, "inv_mult")


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000, debug=False)
