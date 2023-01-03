#!/usr/bin/env python
import socket

import requests
import solcx
from eth_account import Account
from eth_account.datastructures import SignedMessage
from eth_account.messages import encode_defunct, SignableMessage
from eth_typing import Address
from hexbytes import HexBytes
from solcx import compile_files
from web3 import Web3, HTTPProvider
from web3.contract import Contract
from web3.middleware import construct_sign_and_send_raw_middleware
from web3.types import ABI

HOST = "92083232-3813-491b-94e9-720ff8ff5f3c.rdocker.vuln.land"
PORT = 8545

SETUP_ADDR = 0xdA645B4aE6629fEb1C4cad512DF0c15B7F3C6795
PRIVATE_KEY = 0xb837380e8782b15991db9dcb76d3cba5a73785599ae635964ed73795594f5343

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


def deploy_helper_contract(w3: Web3, own_addr: Address) -> (Address, ABI):
    compiled_sol = compile_files("./LudusHelper.sol", output_values=['abi', 'bin'])
    contract_id, contract_interface = compiled_sol.popitem()
    bytecode = contract_interface['bin']
    abi = contract_interface['abi']
    LudusHelper = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = LudusHelper.constructor().transact(transaction={"from": own_addr})
    print(f"TX hash: {tx_hash.hex()}")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_addr = tx_receipt.contractAddress
    return contract_addr, abi


def get_setup_contract(w3: Web3):
    compiled_sol = compile_files("./Setup.sol", output_values=['abi'])
    contract_id, contract_interface = compiled_sol.popitem()
    abi = contract_interface['abi']
    setup = w3.eth.contract(address=SETUP_ADDR.to_bytes(20, "big"), abi=abi)
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


def get_signer_address(w3: Web3, chall_addr: Address):
    challenge = get_challenge_contract(w3, chall_addr)
    signer = challenge.functions.signer().call()
    print(f"Signer: {signer}")


def invoke_challenge(w3: Web3, chall_address: Address, msg: SignableMessage, signature: bytes, own_addr: str):
    joined = b'\x19' + msg.version + msg.header + msg.body
    challenge = get_challenge_contract(w3, chall_address)
    # for i in range(256):
    for i in range(1, 2):
        helper_addr = f"0x00000000000000000000000000000000000000{format(i, '02x')}"
        try:
            # print(w3.eth.get_storage_at(helper_addr, 0))
            # print(w3.eth.get_code(helper_addr))
            print(f"Trying to solve at {helper_addr}:")
            # print(challenge.encodeABI(fn_name="solve", args=[helper_addr, signature.encode(), msg.encode()]))
            solve = challenge.functions.solve(
                # "0"*19*2 + str(int(helper_address, 0)) ,#ChecksumAddress(f"0x{helper_address.replace('0x', '0'*20*2)}".encode()),
                helper_addr,
                signature,
                joined
            )
            # solve.call()
            solve.transact({"from": own_addr})
        except ValueError as e:
            print(e)
    # TODO: Why is it failing here with "revert helper has not enought 0s"? How can we get the helper address to pass this test?


def invoke_helper_solve(helper: Contract, msg: SignableMessage, signature: bytes) -> str:
    joined = b'\x19' + msg.version + msg.header + msg.body
    result = helper.functions.solve(
        "0x0000000000000000000000000000000000000001",
        signature,
        joined,
    ).call()
    return result[1].hex()


def invoke_helper_check(helper: Contract, msg: SignableMessage, signature: bytes) -> str:
    joined = b'\x19' + msg.version + msg.header + msg.body
    result = helper.functions.check(
        "0x0000000000000000000000000000000000000001",
        signature,
        joined,
    ).call()
    return result.hex()

def invoke_one(w3: Web3, msg: SignableMessage, signature: bytes) -> bytes:
    joined = b'\x19' + msg.version + msg.header + msg.body
    hash = Web3.keccak(joined)
    r = signature[:32]
    s = signature[32:64]
    v = b'\00'*31 + b'\x1c'
    response = w3.eth.call({
        "to": "0x0000000000000000000000000000000000000001",
        "value": 0,
        "gas": 20000000000,
        'maxFeePerGas': 2000000000, 'maxPriorityFeePerGas': 1000000000,
        "data": hash + v + r + s
    })
    return response

def check_solved(w3: Web3):
    setup = get_setup_contract(w3)
    solved = setup.functions.isSolved().call()
    print(f"Is solved? {solved}")


def list_blocks_and_transactions(w3: Web3):
    parent_block = "latest"
    while parent_block != HexBytes("0x0000000000000000000000000000000000000000000000000000000000000000"):
        block = w3.eth.get_block(parent_block)
        # print(w3.eth.get_proof(SANTA_COIN, [0], block["number"]))
        # print(block)
        parent_block = block["parentHash"]

        transactions = block["transactions"]
        for t in transactions:
            print("+--> ", end="")
            transaction = w3.eth.get_transaction(t)  # get_raw_transaction
            print(transaction)


def main():
    ip_addr = socket.gethostbyname(HOST)
    print(ip_addr)
    w3 = Web3(HTTPProvider(f"http://{ip_addr}:{PORT}"))

    w3.eth.set_gas_price_strategy(gas_price_strategy=lambda w3, o: Web3.toWei(20000000000, "Wei"))

    account = Account.from_key(PRIVATE_KEY)
    print(f"My own account address: {account.address}")
    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))

    print(f"Current balance: {w3.eth.get_balance(account.address)}")

    helper_address, abi = deploy_helper_contract(w3, account.address)
    print(f"Helper address: {helper_address}")

    helper = w3.eth.contract(address=helper_address, abi=abi)

    # encoded = helper.functions.test(
    #     b"ludus_",
    #     b"0x4d559d6b4f9fdb3a68116eafc5e58eb05984dc4acdd6d093759e791aca846f1a79f5ea51428e94ab82c8b145c5f238b431498ff94394f27ab637be3246560e1b1b"
    # ).call()
    # print(f"Encoded: {encoded.hex()}")
    # print(helper.functions.test2(helper_address).call().hex())
    pub_key_x = PRIVATE_KEY * Secp256k1.Gx % Secp256k1.n
    pub_key_y = PRIVATE_KEY * Secp256k1.Gy % Secp256k1.n

    MESSAGE = "test"
    signed_message: SignedMessage = w3.eth.account.sign_message(encode_defunct(MESSAGE.encode()),
                                                                private_key=PRIVATE_KEY.to_bytes(32, "big"))

    print(f"Signed message:\n"
          f"msg-hash: {signed_message.messageHash.hex()}\n"
          f"r:        {signed_message.r.to_bytes(32, 'big').hex()}\n"
          f"s:        {signed_message.s.to_bytes(32, 'big').hex()}\n"
          f"v:        {signed_message.v}\n"
          f"signature:{signed_message.signature.hex()}")

    result = helper.functions.solve(
        "0x0000000000000000000000000000000000000001",
        signed_message.signature,
        MESSAGE.encode(),
    ).call()
    # ).transact({"from": account.address})
    print(f"Recovery 0x01 - should be {account.address}: {result[1].hex()}")
    # print(result.hex())

    message = encode_defunct(text=MESSAGE)
    print(
        f"Recovery local - should be {account.address}: {w3.eth.account.recover_message(message, signature=signed_message.signature)}")

    print()

    r = requests.get(f"http://{HOST}:8080/sign?msg={MESSAGE}")
    d = r.json()
    msg = d["msg"]
    sig_str = d["signature"]
    sig_bytes = bytes.fromhex(sig_str[2:])
    print(f"Message: {msg}")
    print(f"Signature: {sig_str}")
    print(f"Recovered (santa I): {w3.eth.account.recover_message(encode_defunct(text=msg), signature=sig_bytes)}")
    # print(
    #     f"Recovered (santa I): {w3.eth.account.recover_message(encode_defunct(text=msg), sig_bytes[0:-2] + b'\x1c')}")
    print(f"Orig. signature: {sig_str}")

    print(f"One says: {invoke_one(w3, encode_defunct(text=msg), sig_bytes).hex()}")

    print("With orig. sig: " + invoke_helper_solve(helper, encode_defunct(text=msg), sig_bytes))
    print("With orig. sig (check): " + invoke_helper_check(helper, encode_defunct(text=msg), sig_bytes))
    # print(Web3.keccak(text=msg).hex())

    (r, s, v) = (sig_bytes[0:32], sig_bytes[32:64], sig_bytes[-1:])
    s_int = int.from_bytes(s, "big")
    s_prim = (Secp256k1.n - s_int) % Secp256k1.n
    s_check = (Secp256k1.n - s_prim) % Secp256k1.n
    print(f"Checking signature op: {s_int == s_check}")
    s_prim_hex = s_prim.to_bytes(32, 'big')
    v_int = int.from_bytes(v, "big")
    v_prim = 27 + 28 - v_int
    v_prim_hex = v_prim.to_bytes(1, "big")
    signature_mod: bytes = r + s_prim_hex + v_prim_hex

    print(f"Changed signature: {signature_mod.hex()}")
    print(
        f"Recovered (santa II): {w3.eth.account.recover_message(encode_defunct(text=msg), signature=signature_mod)}")
    print(f"One says: {invoke_one(w3, encode_defunct(text=msg), signature_mod).hex()}")
    print("With mod sig.: " + invoke_helper_solve(helper, encode_defunct(text=msg), signature_mod))

    challenge_address = find_challenge_address(w3)
    get_signer_address(w3, challenge_address)
    invoke_challenge(w3, challenge_address, encode_defunct(text=msg), signature_mod, account.address)

    check_solved(w3)

    # print(w3.eth.get_storage_at(SETUP_ADDR, 0).hex())
    # print(w3.eth.get_storage_at("0x00274528b9ca9977eaafa3b692f4acf849cf944", 0))

    list_blocks_and_transactions(w3)


if __name__ == "__main__":
    # contract()
    main()
