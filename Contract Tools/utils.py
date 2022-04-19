import requests
from web3 import Web3
from config import BLOCK_EXPLORER

# Doesn't really make sense to write a new function just to abstract out the settings based on chain.
# Is there another way ard this? Maybe thru global variables?


def getABI(cid, chain):
    moralis = Web3(
        Web3.WebsocketProvider(BLOCK_EXPLORER[chain]["websocket"])
    )  # moralis API
    url = f'{BLOCK_EXPLORER[chain]["endpoint"]}/api?module=contract&action=getabi&address={cid}&apikey={BLOCK_EXPLORER[chain]["apikey"]}'
    response = requests.request("GET", url)
    return response.json()["result"]


def initialise_contract(cid, chain):
    moralis = Web3(
        Web3.WebsocketProvider(BLOCK_EXPLORER[chain]["websocket"])
    )  # moralis API
    abi = getABI(cid)
    contract = moralis.eth.contract(address=moralis.toChecksumAddress(cid), abi=abi)
    return contract


def get_creation_txn(addr, chain):
    url = f'{BLOCK_EXPLORER[chain]["endpoint"]}/api?module=account&action=txlist&address={addr}&startblock=0&endblock=99999999&page=1&offset=10&sort=ascsort=asc&apikey={BLOCK_EXPLORER[chain]["apikey"]}'
    response = requests.request("GET", url)
    return response.json()["result"][0]


def query_function(cid, function, bid="latest"):
    contract = initialise_contract(cid)
    result = f"contract.functions.{function}.call(block_identifier = {bid})"
    return result

