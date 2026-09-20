import sqlite3
import csv

DB_NAME = "samsung_ledger.db"
CSV_FILE = "ledger_export.csv"

def export_to_csv():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Query all transaction data ordered by timestamp
    cursor.execute("SELECT tx_hash, timestamp, amount, value_usd, method FROM transactions ORDER BY timestamp DESC;")
    rows = cursor.fetchall()
    
    if not rows:
        print("[-] No transaction records found in the database to export.")
        conn.close()
        return

    # Write to CSV
    try:
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(["Transaction Hash (SHA)", "Timestamp (UTC)", "Amount", "Value (USD)", "Method"])
            # Write data rows
            writer.writerows(rows)
            
        print(f"[+] Successfully exported {len(rows)} record(s) to {CSV_FILE}.")
    except Exception as e:
        print(f"[-] Error writing CSV file: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    export_to_csv()
