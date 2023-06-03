import json


def separate_datasets(data):
  """
    Separate data into two datasets and write them to JSON files.

    Args:
        data (dict): The input data dictionary.

    Returns:
        float: The yearly reward rate from the second dataset.
    """
  dataset1 = {}
  dataset2 = {}

  # Splitting the data into two datasets
  dataset1["timestamp"] = data["timestamp"]
  dataset1["totalEmissions"] = data["totalEmissions"]

  if "rewardRatesHistory" in data:
    dataset2["timestamp"] = data["rewardRatesHistory"]["timestamp"]
    dataset2["rates"] = data["rewardRatesHistory"]["rates"]

  # Write the data to the JSON files
  with open("data/policy/dbr_claim.json", "w") as file:
    json.dump(dataset1, file)

  with open("data/policy/dbr_policy.json", "w") as file:
    json.dump(dataset2, file)

  return get_newest_data(dataset2)


def get_newest_data(data):
  """
    Retrieve the newest data based on timestamp from the input data.

    Args:
        data (dict): The input data dictionary.

    Returns:
        float: The yearly reward rate from the newest data.
    """
  rates = data["rates"]
  newest_rate = max(rates, key=lambda x: x["timestamp"])

  newest_data = {}
  newest_data["timestamp"] = newest_rate["timestamp"]
  newest_data["rates"] = [newest_rate]

  yearly_reward_rate = newest_data['rates'][0]['yearlyRewardRate']

  return yearly_reward_rate


def dbr_price(data):
  """
    Retrieve the DBR price from the input data.

    Args:
        data (dict): The input data dictionary.

    Returns:
        float: The DBR price.
    """
  p = data["price"]
  return p
