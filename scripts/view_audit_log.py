import sqlite3

DB_PATH = "local_audit.db"

def view_logs():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Fetch all records from parsed_records table
        cursor.execute('''
            SELECT id, source_institution, asset_title, valuation, compliance_standard, status, ingested_at 
            FROM parsed_records 
            ORDER BY id DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        
        print("=" * 95)
        print(f"       LOCAL SQLITE AUDIT DATABASE REGISTRATIONS ({len(rows)} records found)")
        print("=" * 95)
        print(f"{'ID':<4} | {'Source':<18} | {'Details':<22} | {'Valuation':<10} | {'Status':<8} | {'Timestamp'}")
        print("-" * 95)
        
        for row in rows:
            record_id, source, title, valuation, standard, status, timestamp = row
            # Clean up timestamp string for display
            short_time = timestamp.split(".")[0] if timestamp else "N/A"
            print(f"{record_id:<4} | {source:<18} | {title:<22} | {valuation:<10} | {status:<8} | {short_time}")
            
        print("=" * 95)
        
    except sqlite3.OperationalError:
        print("[INFO] No SQLite database found yet. Run node_health_audit.py first to generate records.")

if __name__ == "__main__":
    view_logs()
