from worker import process_file

# Submit a task with an example IPFS hash (replace with actual hash)
result = process_file.delay("Qmegv4P3TFxMBcghrmtFZ1ZqDMEmToe3nF98j9dLTXaCmP")
print(f"Task submitted! Task ID: {result.id}")
