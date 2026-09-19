import json
import os

TRACKING_FILE = 'bridge_activity.json'

def summarize_volume():
    if not os.path.exists(TRACKING_FILE):
        print(f"Error: {TRACKING_FILE} not found.")
        return
        
    try:
        with open(TRACKING_FILE, 'r') as f:
            records = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return
        
    total_volume = sum(item.get('amount_usd', 0.0) for item in records)
    transaction_count = len(records)
    
    print("=== Bridge Volume Summary ===")
    print(f"Total Transactions Logged: {transaction_count}")
    print(f"Cumulative Aggregate Volume: ${total_volume:,.2f} USD\n")
    
    # Determine Fee Tier based on standard thresholds
    if total_volume > 7_000_000_000:
        tier = "Tier 6 (>7B)"
    elif total_volume > 2_000_000_000:
        tier = "Tier 5 (>2B)"
    elif total_volume > 500_000_000:
        tier = "Tier 4 (>500M)"
    elif total_volume > 100_000_000:
        tier = "Tier 3 (>100M)"
    elif total_volume > 25_000_000:
        tier = "Tier 2 (>25M)"
    elif total_volume > 5_000_000:
        tier = "Tier 1 (>5M)"
    else:
        tier = "Tier 0 (Base Rate)"
        
    print(f"Current Estimated Tier: {tier}")

if __name__ == '__main__':
    summarize_volume()

