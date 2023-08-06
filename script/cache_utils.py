from concurrent.futures import ThreadPoolExecutor

from flask_caching import Cache
from apscheduler.schedulers.background import BackgroundScheduler
import script.shared_utils as shared_utils

CACHE_UPDATE_INTERVAL_MINUTES = 10

cache = Cache(
  config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'data/cache',
    'CACHE_DEFAULT_TIMEOUT': 0,  # Cache data for a month
    'CACHE_THRESHOLD': 0  # Cache up to 100k items
  })

executor = ThreadPoolExecutor(max_workers=5)


def update_cache(api_functions, cache):
  for name, (func, url, alias, keys) in api_functions.items():
    try:
      # Get new data asynchronously
      future = executor.submit(func)

      # If new data is different from current data, update the cache
      if future.result() != cache.get(name):
        cache.set(name,
                  future.result(),
                  timeout=CACHE_UPDATE_INTERVAL_MINUTES * 60)  # Set TTL

    except Exception as e:
      print(f"Error updating cache for {name}: {e}")


def configure_caching(app):
  cache.init_app(app)
  api_functions = shared_utils.load_functions_from_config(
    "api_func_config.json")

  # Schedule the update_cache function to run at the specified interval
  scheduler = BackgroundScheduler()
  scheduler.add_job(lambda: update_cache(api_functions, cache),
                    'interval',
                    minutes=CACHE_UPDATE_INTERVAL_MINUTES)
  scheduler.start()

  return api_functions, cache
