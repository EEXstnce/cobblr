import requests
import json
import datetime


def debt_histo():
    url = "https://www.inverse.finance/api/f2/debt-histo"
    response = requests.get(url)
    data = response.json()

    debts = data["debts"]
    timestamps = data["timestamps"]

    # Get the maximum length among blocks, debts, and timestamps
    max_length = max(len(debts), len(timestamps))

    # Fill the missing elements with None for alignment
    debts += [[None] * 4] * (max_length - len(debts))
    timestamps += [None] * (max_length - len(timestamps))

    # Create a list of dictionaries for aligned data
    aligned_data = []
    next_timestamp = 0
    for i in range(max_length):
        sum_debt = 0
        for j in range(4):
            sum_debt += debts[i][j]
        if i == 0:
            next_timestamp = timestamps[i + 1]
        elif i == max_length - 1:
            next_timestamp = timestamps[i]  # set next_timestamp to current timestamp
        else:
            next_timestamp = timestamps[i + 1]
        aligned_data.append({
            'debts': debts[i],
            'sum_debt': sum_debt,
            'count_second': next_timestamp - timestamps[i],
            'timestamp': datetime.datetime.fromtimestamp(timestamps[i]).strftime('%Y-%m-%d %H:%M:%S'),
        })
        next_timestamp = timestamps[i]


    formatted_data = json.dumps(aligned_data)

    return aligned_data
