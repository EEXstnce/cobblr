import json

def separate_datasets(data):
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
      
  
    return dataset1, dataset2

def get_newest_data(data):
    rates = data["rates"]
    newest_rate = max(rates, key=lambda x: x["timestamp"])
    
    newest_data = {}
    newest_data["timestamp"] = newest_rate["timestamp"]
    newest_data["rates"] = [newest_rate]
    
    return newest_data

