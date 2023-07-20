import script.shared_utils as shared_utils


def load_api_functions():
  api_functions = shared_utils.load_functions_from_config(
    "api_func_config.json")
  return api_functions
