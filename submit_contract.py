import os
from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants
from eth_account import Account

# Load your wallet using your private key
# Replace "YOUR_PRIVATE_KEY" with your actual hex private key (starting with 0x)
private_key = "YOUR_PRIVATE_KEY"
account = Account.from_key(private_key)

# Initialize the Exchange client for Mainnet (use constants.TESTNET_API_URL if testing)
exchange = Exchange(account, base_url=constants.MAINNET_API_URL)

# Construct the action payload matching your interface
action = {
    "type": "requestEvmContract",
    "token": 1,  # Replace with your target token index
    "address": "0x9b498c3c8a0b8cd8ba1d9851d40d186f1872b44e",  # Replace with your EVM contract address
    "evmExtraWeiDecimals": 13  # Calculated difference
}

# Sign and submit the L1 action
response = exchange.submit_l1_action(action)
print(response)
