# [HV22.06] privacy isn't given

<table>
  <tr>
    <th>Categories</th>
    <td>Exploitation</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>easy</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>HaCk0</td>
  </tr>
</table>

## Description
As every good IT person, Santa doesn't have all his backups at one place. Instead, he spread them all over the world.
With this new blockchain unstoppable technology emerging (except Solana, this chain stops all the time) he tries to use it as another backup space. To test the feasibility, he only uploaded one single flag. Fortunately for you, he doesn't understand how blockchains work.

Can you recover the flag?

----

### Information
Start the Docker in the Resources section. You will be able to connect to a newly created Blockchain. Use the following information to interact with the challenge.

Wallet public key 0x28a8746e75304c0780e011bed21c72cd78cd535e
Wallet private key 0xa453611d9419d0e56f499079478fd72c37b251a94bfde4d19872c44cf65386e3
Contract address: 0xe78A0F7E598Cc8b0Bb87894B0F60dD2a88d6a8Ab

The source code of the contract is the following block of code:

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

contract NotSoPrivate {
    address private owner;
    string private flag;

    constructor(string memory _flag) {
        flag = _flag;
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function setFlag(string calldata _flag) external onlyOwner {
        flag = _flag;
    }
}
```

## Solution
Read the flag from the blockchain storage directly by reading out data from the address at which the contract in question is located at.

### Solver
```
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://152.96.7.11:8545'))
r = w3.eth.get_storage_at('0xe78A0F7E598Cc8b0Bb87894B0F60dD2a88d6a8Ab', 1)
print(bytes(r).decode('UTF-8'))
```

## Notes

Tools:
- Metamask https://metamask.io/
- Remix https://remix.ethereum.org/

Core issue: Even though the flag field was marked `private`, this has no influence on the data visibility. [Blockchains and smart contracts are always public](https://docs.soliditylang.org/en/latest/security-considerations.html#private-information-and-randomness). Therefore, we are able to simply read the flag value at the indicated address.


## Flag
```
HV22{Ch41nS_ar3_Publ1C}
```
