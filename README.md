Initial Install and setup for celery and redis

brew install python

python3 -m venv myenv
source myenv/bin/activate

pip install celery redis

brew install redis

brew services start redis

redis-cli ping

# Expected output: PONG

Run a celery worker
celery -A tasks worker --loglevel=info

Run a test task
python test_tasks.py

Install IPFS and run it

brew install ipfs

ipfs init

ipfs daemon

echo "Hello, Web3!" > hello.txt

ipfs add hello.txt
Example output:
text
added QmXnnyufdzAWLh9qZr6nKqeY9D5v4Qm3zQd8iXgVj6hZ9h hello.txt
Note the CID (Content Identifier) returned by the command (e.g., QmXnnyufdzAWLh9qZr6nKqeY9D5v4Qm3zQd8iXgVj6hZ9h). This CID is unique and represents your file on the IPFS network.

Retrieve the file locally:
bash
ipfs cat <CID>

If you want to download the file as a new file:
bash
ipfs get <CID>

Open this URL in your browser:
text
<https://ipfs.io/ipfs/><CID>

By default, files added to an IPFS node are not guaranteed to persist indefinitely unless they are pinned. Pinning ensures that your node keeps a copy of the file.
Pin the file to your local node:
bash
ipfs pin add <CID>

Verify pinned files:
bash
ipfs pin ls --type=recursive

Write contract in solidity

npm install -g truffle
truffle version

mkdir truffle-project && cd truffle-project
truffle init

truffle compile - Run in all terminals
npm install -g ganache-cli

ganache-cli --deterministic --accounts=10 --defaultBalanceEther=1000
truffle migrate --network development

pip install web3

python submit_task.py
