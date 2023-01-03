#!/usr/bin/env python
import socket

import requests
import solcx
from eth_account import Account
from eth_account.messages import encode_defunct, SignableMessage
from eth_typing import Address
from solcx import compile_files
from web3 import Web3, HTTPProvider
from web3.middleware import construct_sign_and_send_raw_middleware

HOST = "5207f4c1-a4ef-41ca-ba1a-ff922a43acce.rdocker.vuln.land"
PORT = 8545

SETUP_ADDR = 0xA13973bb0Ad02178fD006e684Db2737bFd40d2b4
PRIVATE_KEY = 0xfb4719a0df214ce2148972025a9c06a5f155a84d0f7fb2c30d8c2a4f0533190d

MESSAGE = "test"

SOLC_VERSION = "0.8.16"
from solcx import install_solc

install_solc(version=SOLC_VERSION)
solcx.set_solc_version(SOLC_VERSION)


class Secp256k1:
    Gx: int = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
    Gy: int = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    n: int = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    p: int = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
    a: int = 0
    b: int = 7


def get_setup_contract(w3: Web3):
    compiled_sol = compile_files("./Setup.sol", output_values=['abi'])
    contract_id, contract_interface = compiled_sol.popitem()
    abi = contract_interface['abi']
    setup = w3.eth.contract(address=Address(SETUP_ADDR.to_bytes(20, "big")), abi=abi)
    return setup


def find_challenge_address(w3: Web3) -> Address:
    setup = get_setup_contract(w3)
    chall_addr = setup.functions.challenge().call()
    print(f"Challenge address: {chall_addr}")
    return chall_addr


def get_challenge_contract(w3: Web3, chall_address: Address):
    compiled_sol = compile_files("./Challenge.sol", output_values=['abi'])
    contract_id, contract_interface = compiled_sol.popitem()
    abi = contract_interface['abi']
    challenge = w3.eth.contract(address=chall_address, abi=abi)
    return challenge


def invoke_challenge(w3: Web3, chall_address: Address, msg: SignableMessage, signature: bytes, own_addr: str):
    joined = b'\x19' + msg.version + msg.header + msg.body
    challenge = get_challenge_contract(w3, chall_address)
    helper_addr = f"0x0000000000000000000000000000000000000001"
    try:
        print(f"Solving at {helper_addr}:", end=" ")
        solve = challenge.functions.solve(
            helper_addr,
            signature,
            joined
        )
        solve.transact({"from": own_addr})
        print("Done.")
    except ValueError as e:
        print(e)


def check_solved(w3: Web3):
    setup = get_setup_contract(w3)
    solved = setup.functions.isSolved().call()
    print(f"Is solved? {solved}")


def main():
    ip_addr = socket.gethostbyname(HOST)
    print(ip_addr)
    w3 = Web3(HTTPProvider(f"http://{ip_addr}:{PORT}"))

    account = Account.from_key(PRIVATE_KEY)
    print(f"My own account address: {account.address}")
    w3.eth.set_gas_price_strategy(gas_price_strategy=lambda w3, o: Web3.toWei(20000000000, "Wei"))
    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))

    r = requests.get(f"http://{HOST}:8080/sign?msg={MESSAGE}")
    d = r.json()
    msg = d["msg"]
    sig_str = d["signature"]
    sig_bytes = bytes.fromhex(sig_str[2:])
    print(f"Message: {msg}")
    print(f"Signature:         {sig_str}")

    v = sig_bytes[-1:]
    r = sig_bytes[0:32]
    s = sig_bytes[32:64]
    s_int = int.from_bytes(s, "big")
    s_prim = (Secp256k1.n - s_int) % Secp256k1.n

    s_prim_hex = s_prim.to_bytes(32, 'big')

    signature_mod: bytes = r + s_prim_hex + v

    print(f"Changed signature: 0x{signature_mod.hex()}")

    challenge_address = find_challenge_address(w3)
    invoke_challenge(w3, challenge_address, encode_defunct(text=msg), signature_mod, account.address)

    check_solved(w3)


if __name__ == "__main__":
    # contract()
    main()
