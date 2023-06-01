import json

def market_extractor(json_file_path):
    """
    Extract asset names and TVLs from a JSON file.

    Args:
        json_file_path (str): The path to the JSON file.

    Returns:
        dict: A dictionary containing asset names and TVLs.
    """
    # Open the JSON file
    with open(json_file_path) as json_file:
        data = json.load(json_file)

    # Extract asset names and TVLs
    asset_data = {}
    for item in data['firmTvls']:
        asset_data[item['market']['name']] = {'name': item['market']['name'], 'tvl': item['tvl']}

    return asset_data

def fixed_extractor(json_file_path):
    """
    Extract asset names and other attributes from a JSON file.

    Args:
        json_file_path (str): The path to the JSON file.

    Returns:
        dict: A dictionary containing asset names and their attributes.
    """
    # Open the JSON file
    with open(json_file_path) as json_file:
        data = json.load(json_file)

    # Extract asset names and other attributes
    asset_data = {}
    for item in data['markets']:
        asset_data[item['name']] = {
            'name': item['name'],
            'price': item['price'],
            'totalDebt': item['totalDebt'],
            'collateralFactor': item['collateralFactor'],
            'dolaLiquidity': item['dolaLiquidity'],
            'dailyLimit': item['dailyLimit'],
            'dailyBorrows': item['dailyBorrows'],
            'borrowPaused': item['borrowPaused'],
            'supplyApy': item['supplyApy'],
            'extraApy': item['extraApy'],
            'supplyApyLow': item['supplyApyLow']
        }

    return asset_data

def merge_data(market_data, fixed_data, merge_point=None):
    """
    Merge market data and fixed data based on asset names.

    Args:
        market_data (dict): The market data dictionary.
        fixed_data (dict): The fixed data dictionary.
        merge_point (str, optional): The merge point attribute name. Defaults to None.

    Returns:
        list: A list of dictionaries containing the merged data.
    """
    merged_data = []

    # Iterate over asset names in market_data
    for index, name in enumerate(market_data):
        if name in fixed_data:
            # Merge the data from both sources using the merge point if provided
            if merge_point:
                merged_item = {**market_data[name], **fixed_data[name]}
                merged_item[merge_point] = name  # Set the merge point in the merged item
            else:
                merged_item = {**market_data[name], **fixed_data[name]}
            merged_item['index'] = index
            merged_data.append(merged_item)

    return merged_data

def merge_positions(data1, data2):
    """
    Merge two data dictionaries based on the index.

    Args:
        data1 (dict): The first data dictionary.
        data2 (dict): The second data dictionary.

    Returns:
        dict: The merged data dictionary.
    """
    # Create a dictionary to store the merged data
    merged_data = {}

    # Merge the data based on the index
    for index, values in data1.items():
        merged_data[index] = {**values, **data2[index]}

    return merged_data

def clean_data(data, asset_name=None):
    """
    Clean data by filtering out unnecessary attributes.

    Args:
        data (dict): The data dictionary to be cleaned.
        asset_name (str, optional): The asset name to filter the data. Defaults to None.

    Returns:
        dict: The cleaned data dictionary.
    """
    cleaned_data = {}

    for index, values in data.items():
        # Filter out by asset name if provided
        if asset_name and values.get('name') != asset_name:
            continue

        cleaned_values = {key: value for key, value in values.items() if key not in ['index', 'collateralFactor']}
        cleaned_data[index] = cleaned_values

    return cleaned_data
