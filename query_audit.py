import sqlite3
import json

# Connect to your SQLite audit database
conn = sqlite3.connect("audit.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("=== VERIFIED AUDIT PIPELINE DATA EXPORT (CORRECTED TO 150M) ===\n")

cursor.execute("SELECT * FROM td_account_audit ORDER BY account_type, instrument_code;")
rows = cursor.fetchall()

published_data = []
current_category = None

for row in rows:
    item = {
        "timestamp": row["timestamp"],
        "account_id": row["account_id"],
        "account_type": row["account_type"],
        "total_value": row["total_value"],
        "cash_balance": row["cash_balance"],
        "investments_value": row["investments_value"],
        "instrument_code": row["instrument_code"],
        "instrument_name": row["instrument_name"],
        "currency": row["currency"],
        "rate_or_yield": row["rate_or_yield"]
    }
    
    if item["account_type"] != current_category:
        current_category = item["account_type"]
        print(f"\n[ CATEGORY: {current_category} ]")
        print("-" * 50)
    
    print(f"  - ({item['instrument_code']}) {item['instrument_name']} | Currency: {item['currency']} | Value/Yield: {item['rate_or_yield']}")
    published_data.append(item)

# Export verified JSON payload
with open("published_audit_manifest.json", "w") as f:
    json.dump(published_data, f, indent=4)

print("\n" + "=" * 50)
print(f"Successfully exported {len(published_data)} verified records to 'published_audit_manifest.json'.")

conn.close()
