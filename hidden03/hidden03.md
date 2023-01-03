# [HV22.H3] Ruprecht's Secret


## Solution
Convert the flag from day 19 (`HV22{__N1c3__You__ARe__Ind33d__}`) to hex:
```
0x485632327b5f5f4e3163335f5f596f755f5f4152655f5f496e643333645f5f7d
```

Use it as a private key in Metamask to import an account (and generate a corresponding public key).

Copy the public key:
```
0x65cCa9C197f6cF1e38628E4dA7305D924466e4fc
```

Search for the public key on etherscan.io, blockscan.com, etc.

Find out that this public key was indeed used on the Goerli Testnet: https://blockscan.com/address/0x65cCa9C197f6cF1e38628E4dA7305D924466e4fc

See input data on the following transaction: https://goerli.etherscan.io/tx/0xb86d27740bec51d186353a5a9d472dcab6ca122becf129d8840c181f5d6de912


## Flag
```
HV22{W31hN4Cht5m4Nn_&C0._KG}
```
