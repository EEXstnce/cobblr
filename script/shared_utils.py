import importlib
import json


def load_functions_from_config(config_file):
  # Load API function and configuration from JSON file
  with open(config_file, "r") as file:
    config_data = json.load(file)

  # Retrieve functions configuration from the loaded data
  functions_config = {
    route: {
      "func": config_data[route]["func"],
      "url": config_data[route]["url"],
      "alias": config_data[route]["alias"] + "." + config_data[route]["func"]
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

  return api_functions
