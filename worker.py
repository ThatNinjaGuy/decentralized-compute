from celery import Celery
import subprocess
from web3 import Web3

# Initialize Celery app
app = Celery("tasks", broker="redis://localhost:6379/0")

# Connect to local blockchain (Ganache)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Contract details (replace with actual address and ABI)
contract_address = "0x5b1869D9A4C187F2EAa108f3062412ecf0526b24"  # Replace with TaskLogger's deployed address
contract_abi = [
    {
        "inputs": [],
        "name": "taskCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "tasks",
        "outputs": [
            {"internalType": "string", "name": "inputHash", "type": "string"},
            {"internalType": "string", "name": "outputHash", "type": "string"},
            {"internalType": "string", "name": "status", "type": "string"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "string", "name": "inputHash", "type": "string"},
            {"internalType": "string", "name": "outputHash", "type": "string"},
            {"internalType": "string", "name": "status", "type": "string"},
        ],
        "name": "logTask",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Ensure the default account is set
w3.eth.defaultAccount = w3.eth.accounts[0]  # Replace with the correct account

private_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"  # Replace with the private key of the default account

print(f"Contract address: {contract.address}")
print(f"Contract functions: {contract.all_functions()}")


def ipfs_cat(ipfs_hash):
    """Fetch file content from IPFS using its hash."""
    try:
        result = subprocess.run(
            ["ipfs", "cat", ipfs_hash], capture_output=True, text=True
        )
        if result.returncode == 0:
            return result.stdout  # File content
        else:
            raise Exception(f"Error fetching file from IPFS: {result.stderr}")
    except Exception as e:
        print(f"IPFS cat error: {e}")
        raise


def ipfs_add(content):
    """Add content to IPFS and return its hash."""
    try:
        # Write content to a temporary file
        with open("temp.txt", "w") as temp_file:
            temp_file.write(content)

        # Add the file to IPFS
        result = subprocess.run(
            ["ipfs", "add", "-Q", "temp.txt"], capture_output=True, text=True
        )
        if result.returncode == 0:
            return result.stdout.strip()  # IPFS hash
        else:
            raise Exception(f"Error adding file to IPFS: {result.stderr}")
    except Exception as e:
        print(f"IPFS add error: {e}")
        raise


@app.task
def process_file(ipfs_hash):
    try:
        # Step 1: Fetch file from IPFS
        file_data = ipfs_cat(ipfs_hash)
        print(f"Fetched file data: {file_data}")

        # Step 2: Process data (e.g., convert to uppercase)
        processed_content = file_data.upper()
        print(f"Processed content: {processed_content}")

        # Step 3: Upload processed content back to IPFS
        result_hash = ipfs_add(processed_content)
        print(f"Processed file uploaded with new IPFS hash: {result_hash}")

        # Step 4: Log task metadata on blockchain
        transaction = contract.functions.logTask(
            ipfs_hash, result_hash, "Completed"
        ).build_transaction(
            {
                "from": w3.eth.defaultAccount,
                "nonce": w3.eth.get_transaction_count(w3.eth.defaultAccount),
                "gas": 2000000,
                "gasPrice": w3.to_wei("50", "gwei"),
            }
        )

        # Sign and send the transaction
        signed_txn = w3.eth.account.sign_transaction(
            transaction, private_key=private_key
        )
        print(f"Signed transaction: {signed_txn}")

        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

        # Wait for the transaction to be mined
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction successful with hash: {tx_receipt.transactionHash.hex()}")

        return result_hash

    except Exception as e:
        print(f"Error processing file: {e}")
        return None
