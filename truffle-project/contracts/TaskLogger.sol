// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TaskLogger {
    struct Task {
        string inputHash;
        string outputHash;
        string status;
    }

    mapping(uint => Task) public tasks;
    uint public taskCount;

    function logTask(string memory inputHash, string memory outputHash, string memory status) public {
        tasks[taskCount] = Task(inputHash, outputHash, status);
        taskCount++;
    }
}