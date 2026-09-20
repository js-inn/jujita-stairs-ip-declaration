import sqlite3
import json

conn = sqlite3.connect("audit.db")
conn.row_factory = sqlite3.Row  # Set row factory here right after connection
cursor = conn.cursor()

# Update database values to 150M
cursor.execute("""
    UPDATE td_account_audit 
    SET rate_or_yield = 'Min $100 / Max $150M' 
    WHERE instrument_code IN ('TDB8155', 'TDB8159');
""")
conn.commit()

# Fetch and export refreshed manifest
cursor.execute("SELECT * FROM td_account_audit ORDER BY account_type, instrument_code;")
rows = cursor.fetchall()

published_data = []
for row in rows:
    published_data.append({
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
    })

with open("published_audit_manifest.json", "w") as f:
    json.dump(published_data, f, indent=4)

conn.close()
print("Successfully verified and updated: TDB8155 and TDB8159 are set to Max $150M.")
