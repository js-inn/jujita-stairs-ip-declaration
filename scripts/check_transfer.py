import urllib.request
import json
import sys

# Example EVM / Ethereum / ERC-20 address format (or replace with your specific address string)
DEFAULT_ADDRESS = "0x06D217600c97129c47418F12289A8B7D44cF-Caa0"

def check_account_activity(address):
    print("=" * 60)
    print(f"       CHECKING BLOCKCHAIN TRANSERS FOR ADDRESS")
    print("=" * 60)
    print(f"Target Address: {address}")
    
    # Using public block explorer/node query patterns
    # For a production pipeline, public JSON-RPC or block explorer APIs return JSON transfer lists.
    url = f"https://api.etherscan.io/v2/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc"
    
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'IP-Declaration-Pipeline/1.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('status') == '1':
                transactions = result.get('result', [])
                print(f"Found {len(transactions)} transaction(s):")
                for tx in transactions[:5]: # Show latest 5
                    print(f" - Hash: {tx.get('hash')}")
                    print(f"   From: {tx.get('from')}")
                    print(f"   To:   {tx.get('to')}")
                    print(f"   Value: {int(tx.get('value', 0)) / 10**18} ETH/Token")
                    print("-" * 40)
            else:
                print(f"[INFO] Response status 0 or notice: {result.get('message', 'No direct records found via public API key requirement.')}")
                print("Tip: You can also inspect raw node state via your rpc_bridge.py script.")
                
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
    print("=" * 60)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ADDRESS
    check_account_activity(target)
