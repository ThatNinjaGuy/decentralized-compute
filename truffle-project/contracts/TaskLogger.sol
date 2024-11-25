// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TaskLogger {
    struct Task {
        string inputHash;
        string outputHash;
        string status;
    }

    // Mapping to store tasks
    mapping(uint => Task) public tasks;

    // Counter to track the number of tasks
    uint public taskCount;

    // Event to log task details
    event TaskLogged(uint indexed taskId, string inputHash, string outputHash, string status);

    // Function to log a new task
    function logTask(string memory inputHash, string memory outputHash, string memory status) public {
        // Store the task in the mapping
        tasks[taskCount] = Task(inputHash, outputHash, status);

        // Emit the TaskLogged event
        emit TaskLogged(taskCount, inputHash, outputHash, status);

        // Increment the task counter
        taskCount++;
    }
}