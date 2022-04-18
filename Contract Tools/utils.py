import requests
from web3 import Web3
from config import BLOCK_EXPLORER


def getABI(cid, chain):
    settings = BLOCK_EXPLORER[chain]
    moralis = Web3(Web3.WebsocketProvider(settings["websocket"]))  # moralis API
    url = f"https://api.etherscan.io/api?module=contract&action=getabi&address={cid}&apikey={BLOCK_EXPLORER[chain]["apikey"]}"
    response = requests.request("GET", url)
    return response.json()["result"]


def initialise_contract(cid, chain):
    moralis = Web3(Web3.WebsocketProvider(BLOCK_EXPLORER[chain]["websocket"]))  # moralis API
    abi = getABI(cid)
    contract = moralis.eth.contract(address=moralis.toChecksumAddress(cid), abi=abi)
    return contract


def get_creation_txn(addr, chain):
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={addr}&startblock=0&endblock=99999999&page=1&offset=10&sort=ascsort=asc&apikey={ETHERSCAN_API_KEY}"
    response = requests.request("GET", url)
    return response.json()["result"][0]


def query_function(cid, function, bid="latest"):
    contract = initialise_contract(cid)
    result = f"contract.functions.{function}.call(block_identifier = {bid})"
    return result


print(get_creation_txn("0x7C9e73d4C71dae564d41F78d56439bB4ba87592f"))
