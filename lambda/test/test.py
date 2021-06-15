import requests
from os import environ
import json
import csv
from urllib.request import urlopen

url = "https://web3api.io/api/v2/addresses/0x4b1a99467a284cc690e3237bc69105956816f762/token-balances/historical"
querystring = {"page":0,"size":"100","startDate":"2020-08-01","endDate":"2021-04-01","tokenAddress":"0x054f76beed60ab6dbeb23502178c52d6c5debe40"}

headers = {
    "x-amberdata-blockchain-id": "ethereum-mainnet",
    "x-api-key": "UAK2c264f10f6d17e9ba6ed2577d15c5dc1"
}

response = requests.request("GET", url, headers=headers, params=querystring)

maxPageNum = response.json()['payload']['totalRecords']
symbolName = response.json()['payload']['records']

#print(symbolName)
with open ('f762-3.json', 'a', encoding="utf-8") as f:
    json.dump(response.json()['payload']['records'],f,indent=2)
    f.close()
