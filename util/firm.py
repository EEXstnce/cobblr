import json


def get_deposits_and_debt(filename):
    """
    Retrieve deposits and debt data from a JSON file.

    Args:
        filename (str): The path to the JSON file.

    Returns:
        dict: A dictionary containing deposits and debt information per market index.
    """
    with open(filename) as file:
        data = json.load(file)

    positions = data["positions"]
    result = {}

    for position in positions:
        market_index = position["marketIndex"]
        if market_index not in result:
            result[market_index] = {"index": market_index, "deposits": 0, "debt": 0}

        result[market_index]["deposits"] += position["deposits"]
        result[market_index]["debt"] += position["debt"]

    return result


def get_inv_deposits(file_path, dbr_per_inv, dbr_fx):
    """
    Retrieve INV deposits and calculate DBR value per year for a given market index.

    Args:
        file_path (str): The path to the JSON file containing position data.
        dbr_per_inv (float): DBR per INV value.
        dbr_fx (float): DBR FX value.

    Returns:
        list: A list of dictionaries containing INV deposit information and calculated DBR value per year.
    """
    with open(file_path) as file:
        data = json.load(file)

    inv_deposits = []
    for position in data["positions"]:
        if position["marketIndex"] == 5:
            row = {
                "User": position["user"],
                "Deposits": position["deposits"],
                "DBR $/year": position["deposits"] * dbr_per_inv * dbr_fx
            }
            inv_deposits.append(row)

    return inv_deposits


def filter_threshold(data, threshold):
    """
    Filter data based on a given threshold value.

    Args:
        data (list): A list of dictionaries containing data to be filtered.
        threshold (float): The threshold value to filter the data.

    Returns:
        list: A list of dictionaries containing filtered data.
    """
    filtered_data = []
    for position in data:
        calculated_deposits = position["DBR $/year"] / 12
        if calculated_deposits > threshold:
            row = {
                "User": position["User"],
                "Deposits": position["Deposits"],
                "DBR $/month": calculated_deposits
            }
            filtered_data.append(row)

    return filtered_data
