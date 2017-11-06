# Script for Transfer ERC20 Tokens

## Usage: 

- Clone this repo 
- pip install -r requirements.txt
- Run geth --rpc --rpcapi="db,eth,net,web3,personal,web3
- ./transferTokens --contractAddress='0x...' --abiFile=abifile.json --csvfile=transfers.csv

The script will connect check the CSV transfer file for 'orderAmount', and 'orderAddress' required fields.  
