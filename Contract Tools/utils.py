import requests
from web3 import Web3
from config import WEBSOCKET_URL, ETHERSCAN_API_KEY 

moralis = Web3(Web3.WebsocketProvider(WEBSOCKET_URL)) # moralis API

def getABI(cid):
    url = f"https://api.etherscan.io/api?module=contract&action=getabi&address={cid}&apikey={ETHERSCAN_API_KEY}"
    response = requests.request("GET", url)
    return response.json()["result"]

def initialise(cid):
    abi = getABI(cid)
    contract = moralis.eth.contract(address=moralis.toChecksumAddress(cid), abi=abi)
    return contract

def get_creation_txn(addr):
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={addr}&startblock=0&endblock=99999999&sort=asc&apikey=3KD7GRGAU3UHUWF2D1KA7WZAUUSRMXKU7X"
    response = requests.request("GET", url)
    return response.json()["result"]
