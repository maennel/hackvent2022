from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://152.96.7.11:8545'))
r = w3.eth.get_storage_at('0xe78A0F7E598Cc8b0Bb87894B0F60dD2a88d6a8Ab', 1)
print(bytes(r).decode('UTF-8'))
