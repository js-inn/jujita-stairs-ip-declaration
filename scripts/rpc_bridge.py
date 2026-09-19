from pytezos import pytezos

# Define the node RPC URI (as seen in your configuration screen)
RPC_NODE_URI = "https://rpc.tzkt.io/mainnet/"

def check_rpc_connection():
    try:
        print(f"Connecting to RPC Node URI: {RPC_NODE_URI}")
        
        # Initialize pytezos client pointing to the target network URI
        pt = pytezos.using(shell=RPC_NODE_URI)
        
        # Fetch current chain head block level and protocol details
        head_header = pt.shell.head.header()
        
        print("=" * 60)
        print("          RPC NODE CONNECTION SUCCESSFUL")
        print("=" * 60)
        print(f"Chain Protocol : {head_header.get('protocol')}")
        print(f"Chain ID       : {head_header.get('chain_id')}")
        print(f"Current Level  : {head_header.get('level')}")
        print(f"Timestamp      : {head_header.get('timestamp')}")
        print("=" * 60)
        
    except Exception as e:
        print(f"[ERROR] Failed to connect to RPC endpoint: {e}")

if __name__ == "__main__":
    check_rpc_connection()
