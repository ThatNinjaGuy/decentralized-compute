const TaskLogger = artifacts.require("TaskLogger");

module.exports = function (deployer) {
  deployer.deploy(TaskLogger);
};
