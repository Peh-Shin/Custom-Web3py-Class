# Takes in a list of cids, and for each cid, go through the events to catch all Upgraded events emitted
# in the history of the cid
# Returns the implementation contract of each upgraded event
# Final data structure:
# {bid1: 'impl1',
#  bid2: 'impl2',
#  ...
# }
import requests
from config import BITQUERY_API_KEY
from utils import get_creation_txn, moralis

def run_query(query):  # A simple function to use requests.post to make the API call.
    headers = {"X-API-KEY": BITQUERY_API_KEY}  # Bitquery API
    request = requests.post(
        "https://graphql.bitquery.io/", json={"query": query}, headers=headers
    )
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(
            "Query failed and return code is {}.      {}".format(
                request.status_code, query
            )
        )


def event_listener(chain, cid, event_name):
    patterns = {
        "EIP-1967": "0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc",
        "EIP-1822": "0xc5f16f0fcc639fa48a6947836d9850f504798523bf8c9a3a87d5876cf622bcf7",
        "Unstructured": "0x7050c9e0f4ca769c69bd3a8ef740bc37934f8e2c036e5a723fd8ee048ed3f8c3",
    }
    cid = moralis.toChecksumAddress(cid)
    implementation_contracts = dict()
    chain = chain_mapping[chain]
    query = f'{{ \
        ethereum(network: {chain}) {{ \
        arguments( \
            smartContractAddress:  {{is: "{cid}"}}, \
            smartContractEvent: {{is: "{event_name}"}}, \
            options: {{desc: "block.height", limit: 999}} ) {{ \
            block{{height}} \
            reference{{address}} \
            }}}}}} \
            '
    result = run_query(query)["data"]["ethereum"]["arguments"]
    if result != None:
        for impl_contract in result:
            implementation_contracts.update(
                {
                    impl_contract["block"]["height"]: impl_contract["reference"][
                        "address"
                    ]
                }
            )

    for pattern, slot in patterns.items():
        first_impl_cid = ""
        try:
            first_impl_cid = moralis.toHex(
                moralis.eth.get_storage_at(
                    cid, slot, block_identifier=result[-1]["block"]["height"] - 1
                )
            )
        except Exception as e:
            print(e)

        if (
            first_impl_cid
            != "0x0000000000000000000000000000000000000000000000000000000000000000"
            and first_impl_cid != None
        ):
            first_impl_cid = first_impl_cid[0:2] + first_impl_cid[26:]
            implementation_contracts.update(
                {int(get_creation_txn(cid)["blockNumber"]): first_impl_cid}
            )
    # checking = {}
    # for key, value in implementation_contracts.items():
    #     block = key - 1
    #     for pattern, slot in patterns.items():
    #         impl_cid = moralis.toHex(
    #             moralis.eth.get_storage_at(cid, slot, block_identifier=block)
    #         )
    #         if (
    #             impl_cid
    #             != "0x0000000000000000000000000000000000000000000000000000000000000000"
    #             and impl_cid != None
    #         ):
    #             impl_cid = impl_cid[0:2] + impl_cid[26:]
    #  s           checking[block] = impl_cid
    return implementation_contracts


print(event_listener("BSC", "0xee7bc7727436d839634845766f567fa354ba8c56", "Upgraded"))
