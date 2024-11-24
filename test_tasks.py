from tasks import add

# Send a task to the Celery worker
result = add.delay(4, 6)

# Print the task result (asynchronous)
print(f"Task ID: {result.id}")
print("Task submitted! Check the Celery worker console for processing.")

# Wait for and retrieve the result
print("Waiting for result...")
print(f"Result: {result.get(timeout=10)}")
