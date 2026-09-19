import sqlite3

DB_PATH = "local_audit.db"

def summarize_portfolio():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get total valuation and asset count
    cursor.execute('SELECT COUNT(*), SUM(valuation), AVG(valuation) FROM parsed_records')
    total_count, total_valuation, avg_valuation = cursor.fetchone()
    
    total_valuation = total_valuation if total_valuation else 0.0
    avg_valuation = avg_valuation if avg_valuation else 0.0

    print("=" * 50)
    print("       DECENTRALIZED IP PORTFOLIO SUMMARY")
    print("=" * 50)
    print(f"Total Ingested Assets : {total_count}")
    print(f"Total Valuation       : ${total_valuation:,.2f}")
    print(f"Average Asset Value   : ${avg_valuation:,.2f}")
    print("-" * 50)
    
    # Breakdown by Compliance Standard
    print("\n[BREAKDOWN BY COMPLIANCE STANDARD]")
    cursor.execute('''
        SELECT compliance_standard, COUNT(*), SUM(valuation) 
        FROM parsed_records 
        GROUP BY compliance_standard
    ''')
    for standard, count, val in cursor.fetchall():
        val = val if val else 0.0
        print(f"  - {standard}: {count} asset(s) | ${val:,.2f}")

    print("=" * 50)
    conn.close()

if __name__ == "__main__":
    summarize_portfolio()
