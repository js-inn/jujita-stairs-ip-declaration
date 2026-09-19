import json
import datetime
import os

TRACKING_FILE = 'bridge_activity.json'

def log_bridge_transaction(tx_hash, amount_usd, source_network, target_network):
    # Use modern timezone-aware UTC datetime to avoid deprecation warnings
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    record = {
        "timestamp": timestamp,
        "tx_hash": tx_hash.strip(),
        "amount_usd": float(amount_usd),
        "source_network": source_network.strip(),
        "target_network": target_network.strip()
    }
    
    data = []
    if os.path.exists(TRACKING_FILE):
        try:
            with open(TRACKING_FILE, 'r') as f:
                data = json.load(f)
        except Exception:
            data = []
            
    data.append(record)
    
    with open(TRACKING_FILE, 'w') as f:
        json.dump(data, f, indent=2)
        
    print(f"\n[SUCCESS] Logged bridge transaction: {record['tx_hash']} (${record['amount_usd']:,.2f} USD)")

if __name__ == '__main__':
    print("--- Bridge Transfer Logger ---")
    h = input("Enter Transaction Hash (press Enter for test): ").strip() or "0x_test_bridge_hash"
    amt = input("Enter USD Amount: ").strip() or "100.00"
    src = input("Source Network (e.g., Ethereum Mainnet): ").strip() or "Ethereum Mainnet"
    tgt = input("Target Network (e.g., Hyperliquid L1): ").strip() or "Hyperliquid L1"
    
    log_bridge_transaction(h, amt, src, tgt)

