# [HV22.23] Code but no code

<table>
  <tr>
    <th>Categories</th>
    <td>Reverse engineering</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>leet</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>HaCk0</td>
  </tr>
</table>

## Description
Santa loves puzzles and hopes you do too ;) Find the secret inputs which fulfil the requirements and gives you the flag.

## Solution
The challenge is served as a small web service, seemingly distributing Santa's dedicated signatures and validating whether we (the one holding the private key) have solved the challenge.

![Santa's signatures](./dec23-page.png)

Via that page, we can download two Solidity contracts:
- [Setup.sol](./Setup.sol)
- [Challenge.sol](./Challenge.sol)

While `Setup.sol` simply deploys `Challenge.sol`, the latter gives more usable hints.

```solidity
function solve(
    address helper,
    bytes memory sig,
    bytes calldata message
) external {
    for (uint256 i = 0; i < 19; i++) {
        require(bytes20(helper)[i] == 0, "helper has not enought 0s");
    }

    bytes32 r;
    bytes32 s;
    uint8 v = 28;
    assembly {
        // first 32 bytes, after the length prefix
        r := mload(add(sig, 32))
        // second 32 bytes
        s := mload(add(sig, 64))
    }

    (bool success, bytes memory result) = helper.call(
        abi.encode(keccak256(message), v, r, s)
    );
    require(success, "helper call failed");
    require(bytes32(result) == bytes32(uint256(uint160(signer))), "Wrong Signer!");
    solved = true;
}
```

It seems that we need to pass a helper address that starts with 19 zeros. Knowing that a usual address is composed by 20 bytes, there's not much left to work with - but enough, as we'll see.

Next, there's this `v` value that's hardcoded to 28, which doesn't stand out initially, but will show to be tricky.

Finally, we'll have to make sure that the result from the call to *helper* is equal to the signer address (which is equivalent to the address having created the `Setup` contract).

To summarise, **we want to find the creator of some signature with value `v` set to 28 via the help of a remote contract, which can only be addressed using a one-byte address.**

### Ecrecover
Let's jump right in with the obvious stuff first: How do get the signer address from a message and its signature?

Ethereum uses the Elliptic Curve Digital Signature Algorithm (ECDSA). Along with [this explanation](https://ethereum.stackexchange.com/a/15774), there's also a (yet insufficient) explanation on the three values `v`, `r` & `s` and how to recover the public key of the signer from these values and the message hash via `ecrecover`.

Perfect, exactly what we need.

In order to validate the single steps, I created my own small contract and invoked the `ecrecover` function from it - no success, though.

Dissecting ECDSA signatures shows, that a signature is the concatenation of `r + s + v` with `r` & `s` being 32 byte values and `v` being a one byte value of either 27 (0x1b) or 28 (0x1c) (other values are possible if I'm not mistaken, but unlikely).

In our case, however, we only ever get signatures with `v = 27` from the provided web UI.
And it seems it is on purpose, as a the initially supplied message seems to have been padded to fulfill this criteria: `test` became `test_` including an underscore suffix.

Yet, the value `v = 28` is hardcoded.

### Signature malleability
It took another amount of time searching the Internet to learn about **signature malleability** to which signatures created with ECDSA are vulnerable. See here: https://coders-errand.com/malleability-ecdsa-signatures/.

In the second section of the article, it says:

> a valid ECDSA signature `(r, s)` can easily be transformed into a different valid signature, `(r, n - s)` for the same data.

In addition to this, I also skimmed through the [previous article](https://coders-errand.com/ecrecover-signature-verification-ethereum/) to learn more about the theory behind.

In addition, I also stumbled on [EIP-2#Rationale](https://eips.ethereum.org/EIPS/eip-2#rationale) which says, that the `s` part of the signature can be changed, so that `v` is 28 (instead of 27 and vice versa).

To do so, simply compute `Secp256k1.n - s`.

So, let's split up the provided signature into `r, s, v` and compute a new valid signature `r, n - s, 28 + 27 - v`.

Again, I tried to validate this locally, as for this minimal step it had to be possible to be validated.

To make validation work I used the `Web3.py` library and ran the following code (find it in my [dec23-debugger.py script](./dec23-debugger.py):

```python
# Expected signer: 0xa359fAc1B77084b708554B8154a646a216F8d89e

msg = "test"
sig_str = "0x851f1fa8f7a3af17be486d791570ea32f60a7b0eead3ac4202945870c799d7280136427a8e64662bd66ea23affc0d53372db3f3ab835faa47d92224206786c6c1b"
sig_bytes = bytes.fromhex(sig_str[2:])
# Prints the expected signer.
print(w3.eth.account.recover_message(encode_defunct(text=msg), signature=sig_bytes))

# Convert signature from (r, s) to (r, -s).
(r, s, v) = (sig_bytes[0:32], sig_bytes[32:64], sig_bytes[-1:])
s_int = int.from_bytes(s, "big")
s_prim = (Secp256k1.n - s_int) % Secp256k1.n
s_prim_hex = s_prim.to_bytes(32, 'big')
v_int = int.from_bytes(v, "big")
v_prim = 27 + 28 - v_int
v_prim_hex = v_prim.to_bytes(1, "big")
signature_mod: bytes = r + s_prim_hex + v_prim_hex

# Also prints the expected signer.
print(w3.eth.account.recover_message(encode_defunct(text=msg), signature=signature_mod))
```

"Luckily" `ecrecover` is vulnerable to that signature malleability vulnerability.

### Precompiled contracts
Next, I focused on the helper contract.
It became clear pretty quickly that providing an own helper contract performing the `ecrecover` operation is a viable approach only if we can address it with an address prefixed by 19 zeros.

Something that's not possible.

The hurdle can be overcome with some (read: a lot of) DuckDuckGo usage (and some hints from fellow hackers, if you don't happen to type in the right words).

After all, we want to learn about **precompiled contracts** ([see here](https://www.evm.codes/precompiled?fork=merge)), which exist at addresses `0x[...]01` - `0x[...]09`.

The contract at `0x00000000000000000001` happens to do precisely the `ecrecover` we're looking for.

### String encoding for signatures
The final struggle seemed endless. For some reason, I was able to recover the signer locally, but not through a contract, when passing in the message "as is".

It is only when digging a bit deeper into what actually happens when invoking the `encode_defunct(...)` function that [we can see](https://github.com/ethereum/eth-account/blob/v0.8.0/eth_account/messages.py#L229):
1. it returns a `SignableMessage` object.
2. this object contains a peculiar prefix being `\x19Ethereum Signed Message:\n<length>` (the first `\x19` byte is added only later in the process).

The peculiar prefix is actually well defined in [EIP-191](https://eips.ethereum.org/EIPS/eip-191).

In a nutshell, the message `test` becomes before signature:
```
\x19Ethereum Signed Message:\n4test
```

It is only by adding this prefix to the message before hashing that the public key recovery also worked out with contracts. 🎉

### Conclusion
For this challenge, I wanted to implement the entire solution in python.
You can find the entire script [over here](./dec23-solver.py).

The following excerpt represents the main function and shows the high level interactions.

```python
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
```

## Notes
### Elliptic curve base equation
```
y^2 = x^3 + ax + b
```

### How ecrecover works
If a point `P = (x, y)` is on the curve, so is a point `P' = (x, -y)`. "This means we always have more than one valid signature."

A signature can be accepted if `x1 == r mod n`. Since `X = (x1, y1)` and `-X = (x1, -y1)` have the same `x1`, two signatures are possible.

Compute point `X`:
```
X = (eG + rQ) / s mod n. 
```

`e`: hash(`m`).
`G`: Generator point, the base point for the elliptic curve. (given)
`r`: Part of the signature.
`Q`: Public key.
`s`: Part of the signature.
`n`: The modulo constant of the curve (given)

`-X` can be computed by changing the sign of `s`. That means that if `(r, s)` is valid, so is `(r, n - s)` under modulo `n`.

To recover the public key `Q`, we can change the equation as follows:
```
Q = (sX - eG) / r mod n
```
`X` is not known at the beginning, but is strongly related to `r`. This is because `x = r + kn` for some integer `k`, where `x` is an element of the field `Fq` . In other words, `x < q`. ([source](https://coders-errand.com/ecrecover-signature-verification-ethereum/))

`q`: Constant defined by the curve (given).

Ethereum uses the curve **secp256k1** which defines:
```
q = 115792089237316195423570985008687907853269984665640564039457584007908834671663
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337

y^2 = x^3 + 7
```

`v = 28` => recId = 1 (means `1 - y is odd, x is finite`, see [source](https://coders-errand.com/ecrecover-signature-verification-ethereum/)).

`sig = (r, s)` where `r` is the x coordinate of a random curve point `kG mod n`.
`s` depends on `r`.
Multiple coordinates map to the same `r`.


## Links
- Explanations on v, r & s values on ETH transactions: https://ethereum.stackexchange.com/questions/15766/what-does-v-r-s-in-eth-gettransactionbyhash-mean
- Derive the public key from the vrs triplet: https://ethereum.stackexchange.com/questions/13778/get-public-key-of-any-ethereum-account
- Mathematical and cryptographic functions: https://docs.soliditylang.org/en/v0.8.17/units-and-global-variables.html#mathematical-and-cryptographic-functions
- Web3.py's web3.eth API: https://web3py.readthedocs.io/en/latest/web3.eth.html
- Precompiled contracts: https://www.evm.codes/precompiled?fork=merge
- Ecrecover signature verification: https://coders-errand.com/ecrecover-signature-verification-ethereum/
- Ecrecover and ECDSA signature malleability: http://coders-errand.com/malleability-ecdsa-signatures/
- Inherent malleability of ECDSA signatures: https://www.derpturkey.com/inherent-malleability-of-ecdsa-signatures/

## Flag
```
HV22{H1dd3N_1n_V4n1Ty}
```
