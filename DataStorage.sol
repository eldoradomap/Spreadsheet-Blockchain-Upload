// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DataStorage {
    struct Data {
        string jsonData;
    }

    Data[] public data;

    // Event to log data addition
    event DataAdded(string jsonData);

    // Function to add data to the contract
    function addData(string memory jsonData) public {
        data.push(Data(jsonData));
        emit DataAdded(jsonData);
    }

    // Function to retrieve data by index
    function getData(uint256 index) public view returns (string memory) {
        require(index < data.length, "Index out of bounds");
        return data[index].jsonData;
    }

    // Function to get the total number of stored data entries
    function getDataCount() public view returns (uint256) {
        return data.length;
    }
}