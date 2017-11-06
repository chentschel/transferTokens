#!/usr/bin/env python

import csv
import json
import web3
import argparse
import logging

from getpass import getpass
from web3 import Web3, HTTPProvider

parser = argparse.ArgumentParser(description='Transfer ERC20 tokens')

parser.add_argument('--contractAddress', help='Contract address', required=True)
parser.add_argument('--abiFile', help='Contract abi JSON file', required=True)
parser.add_argument('--csvfile', help='CSV input file', required=True)

if __name__ == '__main__':

    args = parser.parse_args()

    # Connect to node
    web3ctl = Web3(HTTPProvider('http://localhost:8545'))
    
    print "Accounts: "
    for idx, acc in enumerate(web3ctl.eth.accounts): 
        print '[{}] - {}'.format(idx, acc)

    accIdx = raw_input('Select the account number:')

    fromAddress = web3ctl.eth.accounts[int(accIdx)]
    fromAddressPassword = getpass("Enter your wallet password: ")

    # Unlock Account.
    if not web3ctl.personal.unlockAccount(
        fromAddress, 
        fromAddressPassword
    ):
        print "Can't unlock account."
        exit(1)
    
    with open(args.abiFile, 'r') as fp:
        contractABI = json.load(fp)

    contract = web3ctl.eth.contract(args.contractAddress, abi=contractABI)

    with open(args.csvfile, 'r') as csvfile:
        
        reader = csv.DictReader(csvfile)
        for row in reader:

            # Skip non finished orders
            if 'orderState' in row and row['orderState'] != 'finished': 
                continue

            try:
                amount = Web3.toWei(row['orderAmount'], 'ether')
                toAddress = Web3.toChecksumAddress(row['orderAddress'])
            
            except Exception as e:
                print("Invalid Data. Skipping :: ", e)
                continue

            try:
                print("Transfer to: {} -> {}".format(toAddress, amount))
                ret = contract.transact({'from': fromAddress})\
                              .transfer(toAddress, amount)

                print "\t TX :: ", ret
                
            except Exception as e:
                print("Failed :: ", e)

