pragma solidity ^0.8.0;

contract LudusHelper {

    function gimme(uint amount) external {
        (bool success, ) = payable(msg.sender).call{value: amount}("");
    }

    constructor() {}
    receive() external payable {}

    function call(
        bytes32 hash,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external returns (bool, address){

//  exports.ecrecover = function (msgHash, v, r, s) {
//  var signature = Buffer.concat([exports.setLength(r, 32), exports.setLength(s, 32)], 64)
//  var recovery = v - 27
//  if (recovery !== 0 && recovery !== 1) {
//    throw new Error('Invalid signature v value')
//  }
//  var senderPubKey = secp256k1.recover(msgHash, signature, recovery)
//  return secp256k1.publicKeyConvert(senderPubKey, false).slice(1)
//}
        address addr = ecrecover(hash, v, r, s);

        return (true, addr);


    }

    function test(
        bytes calldata message,
        bytes memory sig
    ) external returns (bytes memory){
        bytes32 r;
        bytes32 s;
        uint8 v = 28;
        assembly {
            // first 32 bytes, after the length prefix
            r := mload(add(sig, 32))
            // second 32 bytes
            s := mload(add(sig, 64))
        }
        return abi.encode(keccak256(message), v, r, s);

    }

    function test2(
        address some
    ) external returns (bytes20){
        return bytes20(some);
    }

    function solve(
        address helper,
        bytes memory sig,
        bytes calldata message
    ) external returns (bool, bytes memory) {
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

        return helper.call(
            abi.encode(keccak256(message), v, r, s)
        );
    }

    function check(
        address helper,
        bytes memory sig,
        bytes calldata message
    ) external returns (bytes memory) {
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

        return abi.encode(keccak256(message), v, r, s);
    }
}
