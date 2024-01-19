import pandas as pd
import json
import os
import asyncio
import time
import numpy as np
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

# Replace with your Avalanche Fuji node URL
avalanche_fuji_url = 'infura...' # Infura key

# Avalanche Fuji chain ID
avalanche_fuji_chain_id = 43113

# Replace with your wallet private key, make sure you are using testnet avax and not mainnet.
wallet_private_key = '1234...'

# Replace with your wallet address
account ='0x...'

# Replace with your smart contract ABI and contract address
contract_abi = [{}]

# Replace with your contract address
original_contract_address = '0x...'
contract_address = Web3.to_checksum_address(original_contract_address)

# Replace with the path to your XLSX file
xlsx_file_path = 'mysheet.xlsx'

# Function to read and parse data from the XLSX file
def parse_xlsx(file_path, start_row=0, chunk_size=10):
    try:
        # Read the file starting from the row after the last processed row
        df = pd.read_excel(file_path, skiprows=range(1, start_row))
        df = df.drop(columns=['Unnamed: 4', '1. Time (Second): timestamp of a day (24 hours)'])

        data_list = []
        for start in range(0, len(df), chunk_size):
            chunk = df.iloc[start:start + chunk_size]
            chunk_list = []
            for _, row in chunk.iterrows():
                data_dict = {}
                for column_name, cell_data in row.items():
                    data_dict[column_name] = cell_data
                chunk_list.append(data_dict)
            data_list.append(chunk_list)

        return data_list

    except Exception as e:
        print(f"Error parsing XLSX file: {str(e)}")
        return []

# Function to send data to the Avalanche Fuji blockchain
async def upload_to_blockchain(data_list):
    try:
        w3 = Web3(HTTPProvider(avalanche_fuji_url))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        current_nonce = w3.eth.get_transaction_count(account)

        # Create a contract instance
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)

        for data_dict in data_list:
            json_data = json.dumps(data_dict)
            print(json_data)
            gas_price = w3.eth.gas_price
            nonce = w3.eth.get_transaction_count(account)

            txn = contract.functions.addData(json_data).build_transaction({
                'chainId': 43113,
                'gas': 2000000,
                'gasPrice': gas_price,
                'nonce': current_nonce,
            })

            current_nonce += 1

            signed_txn = w3.eth.account.sign_transaction(txn, wallet_private_key)
            txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

            # Wait for the transaction to be confirmed 
            receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

            print(f"Data uploaded to Avalanche Fuji blockchain: {json_data} | Transaction hash: {txn_hash.hex()}")

        print("All data uploaded successfully.")

    except Exception as e:
        print(f"Error uploading data to Avalanche Fuji blockchain: {str(e)}")

        # Print more detailed error information
        if hasattr(e, 'response'):
            print("Error response:")
            print(e.response)
        if hasattr(e, 'args'):
            print("Error arguments:")
            print(e.args)



def main(file_path, chunk_size=10, retry_delay=5):
    last_processed_row = 0

    while True:
        try:
            data_list = parse_xlsx(file_path, start_row=last_processed_row, chunk_size=chunk_size)
            if data_list:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(upload_to_blockchain(data_list))
                last_processed_row += len(data_list) * chunk_size
        except (PermissionError, IOError) as e:
            print(f"File access error: {e}, retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break
        # Add a sleep time if you want to wait between checks
        time.sleep(20)

if __name__ == "__main__":
    main('mysheet.xlsx') # Replace with same file path you entered above
