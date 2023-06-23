import functools
import os
import time
import pickle
import json
import importlib

from flask import Flask, request, render_template, jsonify, make_response
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from flask_caching import Cache
from apscheduler.schedulers.background import BackgroundScheduler

from util import printToJson

os.environ['TZ'] = 'UTC'
time.tzset()

app = Flask(__name__)
CORS(app)
cache = Cache(
  app,
  config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'data/cache',
    'CACHE_DEFAULT_TIMEOUT': 2221600,  # Cache data for a month
    'CACHE_THRESHOLD': 100000  # Cache up to 100k items
  })
hits = 0
errors = 0

# Load API function and configuration from JSON file
with open("api_func_config.json", "r") as config_file:
  config_data = json.load(config_file)

# Retrieve functions configuration from the loaded data
functions_config = {
  route: {
    "func": config_data[route]["func"],
    "url": config_data[route]["url"],
    "alias": config_data[route]["alias"]
  }
  for route in config_data
}

api_functions = {}

# Dynamically import functions based on configuration
for route, config in functions_config.items():
  module_name, function_name = config["alias"].rsplit(".", 1)
  module = importlib.import_module(module_name)
  func = getattr(module, function_name)
  api_functions[route] = (func, config["url"], config["alias"])


def update_cache():
  for name, (func, url, alias) in api_functions.items():
    try:
      # Get current data
      current_data = cache.get(name)

      # Get new data
      new_data = func()

      # If new data is different from current data, update the cache
      if new_data != current_data:
        cache.set(name, new_data)

    except Exception as e:
      print(f"Error updating cache for {name}: {e}")


# Schedule the update_cache function to run every minute instead of every 2 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(update_cache, 'interval', minutes=1)
scheduler.start()


@app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def catch_all_options(path):
  return '', 200


@app.route('/favicon.ico')
def favicon():
  return '', 204


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
        auth = True
    else:
      auth = True

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
  cache_key = name.replace("/", "_")  # replace slashes with underscores
  cached_data = cache.get(cache_key)
  if cached_data is not None:
    return cached_data
  else:
    global hits, errors
    hits += 1
    try:
      # Attempt to get data and save to cache
      data = func()
      printToJson(data, cache_key)  # use modified key here
      cache.set(cache_key, data)  # Cache data for a month
      return make_response(jsonify(data), 200)
    except Exception as e:
      # If error, increase error count and try to return cached data
      errors += 1
      print(f"Error fetching {name} data: {e}")
      cached_data = cache.get(cache_key)  # Get cached data if it exists
      if cached_data is not None:
        return make_response(jsonify(cached_data), 200)
      else:
        return make_response(
          jsonify({
            "success":
            False,
            "message":
            f"Error fetching {name} data and no cache is available."
          }), 500)


for route, (func, url, alias) in api_functions.items():
  route_func = functools.partial(endpoint, func, route)
  route_func.__name__ = f"{func.__name__}_endpoint"  # Flask uses the function name as an endpoint
  app.route(route, methods=["GET"])(route_func)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000, debug=False)
