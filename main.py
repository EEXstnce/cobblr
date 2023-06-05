import requests
import os
from flask import Flask, request, render_template, jsonify
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
import pickle

from clean.dbr import dbr_policy, dbr_price
from clean.pce import tvl, firm, combine
from clean.positions import positions

from build.tvl_firm import tvl_firm
from build.dbr_issue import dbr_issue
from build.inv_stake import inv_stake
from build.dbr_inv import dbr_per_inv

from util import printToJson

app = Flask(__name__)
CORS(app, origins=["https://enlighten.gg/"])
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

# Create a folder called "in" to store API endpoint results
if not os.path.exists("in"):
  os.mkdir("in")

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

@app.route("/dbr_policy", methods=["GET"])
def dbr_policy_endpoint():
  global hits, errors
  hits += 1
  url = api_endpoints["dbr_policy"]
  try:
      response = requests.get(url)
      data = response.json()
      data = dbr_policy(data)
      printToJson(data, "dbr_policy")
      return jsonify(data)
  except:
      errors += 1
      return jsonify({"success": False, "message": "Error fetching dbr_policy data"}), 500

@app.route("/dbr_price", methods=["GET"])
def dbr_price_endpoint():
  global hits, errors
  hits += 1
  url = api_endpoints["dbr_price"]
  try:
      response = requests.get(url)
      data = response.json()
      data = dbr_price(data)
      printToJson(data, "dbr_price")
      return jsonify(data)
  except:
      errors += 1
      return jsonify({"success": False, "message": "Error fetching dbr_price data"}), 500

@app.route("/tvl", methods=["GET"])
def tvl_endpoint():
  global hits, errors
  hits += 1
  url = api_endpoints["tvl"]
  try:
      response = requests.get(url)
      data = response.json()
      data = tvl(data)
      printToJson(data, "tvl")
      return jsonify(data)
  except:
      errors += 1
      return jsonify({"success": False, "message": "Error fetching TVL data"}), 500

@app.route("/firm", methods=["GET"])
def firm_endpoint():
  global hits, errors
  hits += 1
  url = api_endpoints["firm"]
  try:
      response = requests.get(url)
      data = response.json()
      data = firm(data)
      printToJson(data, "firm")
      return jsonify(data)
  except:
      errors += 1
      return jsonify({"success": False, "message": "Error fetching firm data"}), 500

@app.route("/positions", methods=["GET"])
def positions_endpoint():
  global hits, errors
  hits += 1
  url = api_endpoints["positions"]
  try:
      response = requests.get(url)
      data = response.json()
      data = positions(data)
      printToJson(data, "positions")
      return jsonify(data)
  except:
      errors += 1
      return jsonify({"success": False, "message": "Error fetching positions data"}), 500

@app.route("/tvl_firm", methods=["GET"])
def tvl_firm_endpoint():
  global hits, errors
  hits += 1
  try:
      data = tvl_firm(api_endpoints)
      printToJson(data, "tvl_firm")
      return jsonify(data)
  except:
      errors += 1
      return jsonify({"success": False, "message": "Error fetching TVL and firm data"}), 500

@app.route("/dbr_issue", methods=["GET"])
def dbr_issue_endpoint():
  global hits, errors
  hits += 1
  try:
      data = dbr_issue(api_endpoints)
      printToJson(data, "dbr_issue")
      return jsonify(data)
  except:
      errors += 1
      return jsonify({"success": False, "message": "Error calculating DBR issuance"}), 500

@app.route("/inv_stake", methods=["GET"])
def inv_stake_endpoint():
  global hits, errors
  hits += 1
  try:
      data = inv_stake(api_endpoints)
      printToJson(data, "inv_stake")
      return jsonify(data)
  except:
      errors += 1
      return jsonify({"success": False, "message": "Error calculating inverted stake"}), 500

@app.route("/dbr_inv", methods=["GET"])
def dbr_inv_endpoint():
  global hits, errors
  hits += 1
  try:
      data = dbr_per_inv(api_endpoints)
      printToJson(data, "dbr_inv")
      return jsonify(data)
  except:
      errors += 1
      return jsonify({"success": False, "message": "Error calculating DBR per inverted stake"}), 500


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000, debug=False)