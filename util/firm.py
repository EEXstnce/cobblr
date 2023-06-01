import json

def get_deposits_and_debt(filename):
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
