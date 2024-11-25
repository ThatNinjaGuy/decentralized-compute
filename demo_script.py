from multiprocessing import Process
import random
import time
from worker import process_file


# Simulate file uploads by generating IPFS-like hashes
def simulate_file_uploads(num_files):
    files = []
    for i in range(num_files):
        # Generate simulated IPFS hashes
        file_hash = f"Qmegv4P3TFxMBcghrmtFZ1ZqDMEmToe3nF98j9dLTXaCmP"
        files.append(file_hash)
    return files


# Worker function to simulate task processing
def worker_process(worker_id):
    print(f"Worker {worker_id} joined the network.")
    while True:
        # Fetch a task from the Celery queue
        task = process_file.AsyncResult()  # Replace with actual method to fetch a task
        if task.ready():
            # Process the task
            result = task.get()  # This will execute the task and get the result
            print(f"Worker {worker_id} processed task with result: {result}")
        else:
            print(f"Worker {worker_id} is waiting for tasks.")
        time.sleep(1)  # Short sleep to prevent busy waiting


# Function to simulate the entire workflow
def simulate_workflow(num_files, num_workers):
    print("Simulating multiple file uploads...")
    files = simulate_file_uploads(num_files)  # Generate tasks (file hashes)
    print(f"Uploaded Files: {files}\n")

    print(f"Creating {num_workers} workers...")
    workers = []
    for i in range(num_workers):
        p = Process(target=worker_process, args=(i,))
        workers.append(p)
        p.start()

    # Submit tasks to the Celery queue
    for file_hash in files:
        result = process_file.delay(file_hash)
        print(f"Task submitted for file {file_hash}! Task ID: {result.id}")
        time.sleep(0.5)  # Add a 500ms delay between task submissions

    # Wait for all workers to complete their tasks
    for worker in workers:
        worker.join()
        print(f"Worker {worker.pid} has completed its tasks.")


# Run the workflow simulation
if __name__ == "__main__":
    num_files = 100  # Number of files (tasks)
    num_workers = 5  # Number of workers
    simulate_workflow(num_files, num_workers)
