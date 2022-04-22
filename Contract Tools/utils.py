import requests
from web3 import Web3
from config import BLOCK_EXPLORER

# Web3py classes

# Qns:
# 1. How does Web3.WebsocketProvider("...") work? How does the Web3 class instantiate a provider object through
# WebsocketProvider method?
# 2. How does (w3 object after __init__).eth.Contract work? How does the web3 object access the eth module in the web3 library?
## Ans?? They imported the WebsocketProvider and ETH classes into the Web3 class itself.
# For (1), calling the WSP class attr in Web3 class will lead to the WSP object, which has to be initialised
# For (2), the get_default_modules() function sets the eth, geth, net attributes to the Web3 object that was initialised.
# The attributes each lead to the ETH, GETH classes themselves

# Lessons learnt: attributes can lead to another class. In this case, know that the brackets you put after
# the attribute is used to init the class, just like the params for constructor function of solidity contracts
# Without any brackets, it means you are either 1. just accessing the class without init anything,
# or 2. there's no init for the class, hence you can create an object of the class directly
class W3_OBJECT(Web3):
    def __init__(self, chain):
        self.chain = chain
        super().__init__(
            super().WebsocketProvider((BLOCK_EXPLORER[chain]["websocket"]))
        )

    def getABI(self, address):
        url = f'{BLOCK_EXPLORER[self.chain]["endpoint"]}/api?module=contract&action=getabi&address={address}&apikey={BLOCK_EXPLORER[self.chain]["apikey"]}'
        self.contract_abi = requests.request("GET", url).json()["result"]
        return self.contract_abi

    @staticmethod
    def function_call(contract, fn_obj):
        def pass_input(*args):
            cid = contract  # Relook at how to change this, and also why can't pass contract object to eval string
            return eval(f"cid.functions.{fn_obj}{args}.call()")

        return pass_input

    def contract(self, address):
        contract = self.eth.contract(address=address, abi=self.getABI(address))
        for function in contract.functions._functions:
            setattr(
                self,
                function["name"],
                self.function_call(  # Why is it still using "self" to call staticmethod?
                    contract, function["name"]
                ),  # Value stored into attribute is the function["name"] object itself that is an input to another_function that allows for user input to be passed in to the function["name"] object
            )
        return self



ETH = W3_OBJECT("ETH")
lp_farm = ETH.contract("0xc2EdaD668740f1aA35E4D8f227fB8E17dcA888Cd")
print(lp_farm.pendingSushi(347, "econbeard.eth"))

# def getABI(cid, chain):
#     moralis = Web3(
#         Web3.WebsocketProvider(BLOCK_EXPLORER[chain]["websocket"])
#     )  # moralis API
#     url = f'{BLOCK_EXPLORER[chain]["endpoint"]}/api?module=contract&action=getabi&address={cid}&apikey={BLOCK_EXPLORER[chain]["apikey"]}'
#     response = requests.request("GET", url)
#     return response.json()["result"]


# def initialise_contract(cid, chain):
#     moralis = Web3(
#         Web3.WebsocketProvider(BLOCK_EXPLORER[chain]["websocket"])
#     )  # moralis API
#     abi = getABI(cid)
#     contract = moralis.eth.contract(address=moralis.toChecksumAddress(cid), abi=abi)
#     return contract


# def get_creation_txn(addr, chain):
#     url = f'{BLOCK_EXPLORER[chain]["endpoint"]}/api?module=account&action=txlist&address={addr}&startblock=0&endblock=99999999&page=1&offset=10&sort=ascsort=asc&apikey={BLOCK_EXPLORER[chain]["apikey"]}'
#     response = requests.request("GET", url)
#     return response.json()["result"][0]


# def query_function(cid, function, bid="latest"):
#     contract = initialise_contract(cid)
#     result = f"contract.functions.{function}.call(block_identifier = {bid})"
#     return result
