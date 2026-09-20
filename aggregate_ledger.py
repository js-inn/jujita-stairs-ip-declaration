import sqlite3

DB_NAME = "samsung_ledger.db"

def summarize_ledger():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Total count and sum metrics
    cursor.execute("SELECT COUNT(*), SUM(amount), SUM(value_usd), AVG(value_usd) FROM transactions;")
    total_count, total_amount, total_usd, avg_usd = cursor.fetchone()
    
    print("=" * 45)
    print("       SAMSUNG WALLET LOCAL LEDGER SUMMARY       ")
    print("=" * 45)
    print(f" Total Transactions Logged : {total_count or 0}")
    print(f" Total Asset Volume        : {total_amount or 0.0:.6f}")
    print(f" Total Value (USD)         : ${total_usd or 0.0:,.2f}")
    print(f" Average Transfer (USD)    : ${avg_usd or 0.0:,.2f}")
    print("-" * 45)
    
    # Recent chronological breakdown
    print(" Recent Activity Breakdown:")
    cursor.execute("SELECT timestamp, amount, value_usd FROM transactions ORDER BY timestamp DESC LIMIT 5;")
    rows = cursor.fetchall()
    for row in rows:
        print(f" [{row[0]}] -> {row[1]} tokens (${row[2]:,.2f})")
    print("=" * 45)
    
    conn.close()

if __name__ == "__main__":
    summarize_ledger()
