import requests


def retrieve():
    # Amberdata query

    # refers to https://docs.amberdata.io/reference#transaction-token-transfers
    url = "https://web3api.io/api/v2/addresses/0x7a9E457991352F8feFB90AB1ce7488DF7cDa6ed5/token-transfers"

    headers = {
        "Accept": "application/json",
        "x-amberdata-blockchain-id": "ethereum-mainnet",
        "x-api-key": "UAK2c264f10f6d17e9ba6ed2577d15c5dc1"
    }

    # here, the time format should be milliseconds, e.g. 1598932800000 (equals to "2020-09-01"), 1619841600000 (equals to "2021-05-01")
    # however, the max time period between startDate and endDate is 2678400000
    # thus, we need to request with a loop for the period "2020-09-01"-"2021-05-01" by storing results into a list "results"

    results = []

    # divide the time period into ten pieces
    timelength = 2090880000
    for i in range(1598932800000, 1619841600000, timelength):
        page = 0
        while True:
            querystring = {"page": page,
                           "size": "1000",
                           "startDate": i,
                           "endDate": i + timelength}
            response = requests.request("GET", url, headers=headers, params=querystring)
            if response.status_code == 200 and response.json()['status'] == 200:
                if len(response.json()['payload']['records']) == 0:
                    break
                else:
                    results.extend(response.json()['payload']['records'])
                    page += 1

    return results
