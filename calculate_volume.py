import sqlite3

DB_FILE = 'corporate_ledger.db'

def calculate_tier_volume():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Query transaction amounts or values stored in your ledger
        # Adjust table/column names based on your specific schema fields
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        total_volume = 0.0
        print("Scanning ledger for volume calculation...\n")
        
        # Example estimation loop across numeric columns
        if 'octopus_transactions' in tables:
            cursor.execute("SELECT * FROM octopus_transactions;")
            rows = cursor.fetchall()
            for r in rows:
                # Look for numeric fields representing amounts/values in the row tuple
                for item in r:
                    try:
                        val = float(item)
                        # Filter for realistic transaction sizes if needed
                        if 10.0 <= val <= 10000.0:
                            total_volume += val
                    except (ValueError, TypeError):
                        continue
                        
        print(f"Estimated Aggregate Volume: ${total_volume:,.2f}")
        
        # Determine Tier based on volume thresholds
        if total_volume > 7_000_000_000:
            print("Current Tier: Tier 6 (>7B)")
        elif total_volume > 2_000_000_000:
            print("Current Tier: Tier 5 (>2B)")
        elif total_volume > 500_000_000:
            print("Current Tier: Tier 4 (>500M)")
        elif total_volume > 100_000_000:
            print("Current Tier: Tier 3 (>100M)")
        elif total_volume > 25_000_000:
            print("Current Tier: Tier 2 (>25M)")
        elif total_volume > 5_000_000:
            print("Current Tier: Tier 1 (>5M)")
        else:
            print("Current Tier: Tier 0 (Base Rate)")
            
        conn.close()
    except Exception as e:
        print(f"Error calculating volume: {e}")

if __name__ == '__main__':
    calculate_tier_volume()

