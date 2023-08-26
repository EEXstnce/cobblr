import importlib
import json


def construct_url(template_url, keys):
    for idx, key in enumerate(keys):
        placeholder = "{" + str(idx) + "}"
        template_url = template_url.replace(placeholder, key)
    return template_url


def load_functions_from_config(config_file):
    # Load API function and configuration from JSON file
    with open(config_file, "r") as file:
        config_data = json.load(file)

    # Retrieve functions configuration from the loaded data
    functions_config = {
        route: {
            "func": config_data[route]["func"],
            "url": construct_url(config_data[route]["url"],
                                 config_data[route]["keys"]),
            "alias": config_data[route]["alias"] + "." +
            config_data[route]["func"],
            "keys": config_data[route]["keys"],
            "config": config_data[route]["config"]
        }
        for route in config_data
    }

    api_functions = {}

    # Dynamically import functions based on configuration
    for route, config in functions_config.items():
        module_name, function_name = config["alias"].rsplit(".", 1)
        module = importlib.import_module(module_name)
        func = getattr(module, function_name)
        api_functions[route] = (func, config["url"], config["alias"],
                                config["keys"], config["config"])

    return api_functions
