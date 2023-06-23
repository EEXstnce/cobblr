import functools
import os
import time
import pickle
import json
import importlib
from apscheduler.schedulers.background import BackgroundScheduler
from flask_caching import Cache

cache = Cache(
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
api_functions = {
  route: {
    "func": config_data[route]["func"],
    "url": config_data[route]["url"],
    "alias": config_data[route]["alias"]
  }
  for route in config_data
}

# Dynamically import functions based on configuration
for route, config in api_functions.items():
  module_name, function_name = config["alias"].rsplit(".", 1)
  module = importlib.import_module(module_name)
  func = getattr(module, function_name)
  api_functions[route]["func"] = func


def update_cache():
  for name, config in api_functions.items():
    try:
      func = config["func"]

      # Get current data
      current_data = cache.get(name)

      # Get new data
      new_data = func()

      # If new data is different from current data, update the cache
      if new_data != current_data:
        cache.set(name, new_data)

    except Exception as e:
      print(f"Error updating cache for {name}: {e}")


def run_scheduler():
  scheduler = BackgroundScheduler()
  scheduler.add_job(update_cache, 'interval', minutes=1)
  scheduler.start()
