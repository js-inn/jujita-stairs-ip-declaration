import urllib.request
import json

# Define the Tezos node RPC URI (as seen in your configuration screen)
RPC_NODE_URI = "https://rpc.tzkt.io/mainnet/chains/main/blocks/head"

def query_rpc_node():
    try:
        print(f"Connecting to RPC Node URI: {RPC_NODE_URI}")
        
        # Make a standard HTTP GET request to the RPC node
        req = urllib.request.Request(
            RPC_NODE_URI,
            headers={'User-Agent': 'IP-Declaration-Bridge/1.0'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            header = data.get('header', {})
            
        print("=" * 60)
        print("          RPC NODE CONNECTION SUCCESSFUL")
        print("=" * 60)
        print(f"Chain Protocol : {header.get('protocol')}")
        print(f"Chain ID       : {data.get('chain_id')}")
        print(f"Current Level  : {header.get('level')}")
        print(f"Timestamp      : {header.get('timestamp')}")
        print("=" * 60)
        
    except Exception as e:
        print(f"[ERROR] Failed to query RPC endpoint: {e}")

if __name__ == "__main__":
    query_rpc_node()
