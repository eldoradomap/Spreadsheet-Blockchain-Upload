# Spreadsheet Blockchain Upload

This project consists of a set of scripts designed to read data from an Excel spreadsheet, format it into JSON, and upload it to the blockchain using the Avalanche Fuji testnet.

## Features

- Read data from XLSX files.
- Convert spreadsheet rows into JSON format.
- Upload JSON data to the Avalanche Fuji blockchain.
- Download JSON data from the Avalanche Fuji blockchain.

## Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.6 or higher
- pip install -r requirements.txt

## Installation

Clone the repository to your local machine:

git clone https://github.com/eldoradomap/spreadsheet-blockchain-upload.git
cd blockchain-data-uploader

## Configuration

Before running the scripts, ensure you have the following configuration in place:

- DataStorage.sol has been deployed to the Avalanche Fuji blockchain.
- Input up your Avalanche Fuji node URL in the script. - Line 11 in both scripts.
- Input your wallet private key in the script. - Line 17 on local parser.
- Input the smart contract ABI and contract address in the script. - Line 26 on the local parser. Line 12 on the destination parser.
- Input file paths - Lines 30 and 124 on the local parser (these should be the path to the spreadsheet you are uploading). Line 183 on the destination parser (this will be where and what name your file is saved to.)

# Usage

Deploy the DataStorage.sol smart contract to the Avalanche Fuji blockchain.

To parse an Excel file and upload the data to the blockchain, run:

```
python LocalParser.py
```

To reconstruct the Excel file from blockchain data, run:

```
python DestinationParser.py
```

Both scripts need to be run in a system that has network access to the Avalanche Fuji testnet.
