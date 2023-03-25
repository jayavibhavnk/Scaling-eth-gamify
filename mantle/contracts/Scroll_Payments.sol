pragma solidity ^0.8.0;

contract FundContract {
    address payable public owner;
    mapping(address => uint256) public balances;

    constructor() {
        owner = payable(msg.sender);
    }

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);
    }

    function transfer(address payable recipient, uint256 amount) external {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        balances[recipient] += amount;
    }

    function close() external {
        require(msg.sender == owner, "Only owner can close the contract");
        selfdestruct(owner);
    }
}
