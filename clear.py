import os
import shutil

cache_directory = "./data/cache"

# Check if the cache directory exists
if os.path.exists(cache_directory) and os.path.isdir(cache_directory):
  # Iterate over the files in the cache directory and delete them
  for filename in os.listdir(cache_directory):
    file_path = os.path.join(cache_directory, filename)
    if os.path.isfile(file_path):
      os.remove(file_path)
    elif os.path.isdir(file_path):
      shutil.rmtree(file_path)

  print("Cache contents deleted successfully.")
else:
  print("Cache directory does not exist.")
