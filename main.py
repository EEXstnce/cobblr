from flask import Flask, request, render_template, jsonify, make_response
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from datetime import timedelta
import functools
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='tzlocal')

from script import cache_utils
from script import api_functions
from script.util import printToJson
from script.authorization import check_authorization
import script.shared_utils as shared_utils

app = Flask(__name__)
CORS(app)

cache_functions = cache_utils.configure_caching(app)
api_functions, cache = cache_utils.configure_caching(app)

hits = 0
errors = 0


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

  auth = check_authorization(token)

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


def endpoint(func, name, cache, keys):
  cache_key = name.replace("/", "_")  # replace slashes with underscores
  cached_data = cache.get(cache_key)

  try:
    # Attempt to get data and save to cache
    data = func(url, keys)
    printToJson(data, cache_key)  # use modified key here
    cache_timeout = int(
      timedelta(days=30).total_seconds())  # Cache data for a month
    cache.set(cache_key, data, timeout=cache_timeout)
    return make_response(jsonify(data), 200)
  except Exception as e:
    # If error, increase error count and try to return cached data
    global errors
    errors += 1
    print(f"Error fetching {name} data: {e}")
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


for route, (func, url, alias, keys) in api_functions.items():
  route_func = functools.partial(endpoint, func, route, cache, keys)
  route_func.__name__ = f"{func.__name__}_endpoint"  # Flask uses the function name as an endpoint
  app.route(route, methods=["GET"])(route_func)

if __name__ == "__main__":
  os.environ['TZ'] = 'UTC'  # Set the timezone to UTC
  app.run(host="0.0.0.0", port=8000, debug=False)