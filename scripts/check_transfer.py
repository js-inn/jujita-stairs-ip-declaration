import urllib.request
import json
import sys

# Standard public JSON-RPC endpoint
DEFAULT_RPC = "https://ethereum-rpc.publicnode.com"
DEFAULT_ADDRESS = "0x06D217600c97129c47418F12289A8B7D44cFCaa0"

def check_rpc_balance(rpc_url, address):
    print("=" * 60)
    print(f"       CHECKING ACCOUNT STATE VIA JSON-RPC")
    print("=" * 60)
    
    # Clean up address formatting (remove trailing dashes if any)
    clean_address = address.strip().replace("-", "")
    print(f"Node RPC : {rpc_url}")
    print(f"Address  : {clean_address}")
    
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [clean_address, "latest"],
        "id": 1
    }
    
    data = json.dumps(payload).encode('utf-8')
    
    try:
        req = urllib.request.Request(
            rpc_url,
            data=data,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Android; Termux)'
            }
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            if 'result' in result:
                wei_balance = int(result['result'], 16)
                eth_balance = wei_balance / 10**18
                print(f"[SUCCESS] Current Balance: {eth_balance} ETH / FOLD-compatible state")
            else:
                print(f"[INFO] Node response error: {result.get('error')}")
                
    except Exception as e:
        print(f"[ERROR] RPC connection failed: {e}")
    print("=" * 60)

if __name__ == "__main__":
    target_address = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ADDRESS
    check_rpc_balance(DEFAULT_RPC, target_address)
