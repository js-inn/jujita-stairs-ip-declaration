import sqlite3
import os

DB_PATH = "/storage/emulated/0/Government_Contracts_Compliance/compliance_pipeline.db"

def view_wire_logs():
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] Compliance database not found at {DB_PATH}")
        return
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check tables available
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"\n[INFO] Connected to compliance pipeline database.")
    print(f"[INFO] Available tables: {tables}\n")
    
    if "wire_reconciliation" in tables:
        cursor.execute("SELECT * FROM wire_reconciliation")
        rows = cursor.fetchall()
        print("==========================================")
        print(" WIRE RECONCILIATION LOGS")
        print("==========================================")
        if not rows:
            print("No wire records found.")
        else:
            for idx, row in enumerate(rows, 1):
                print(f"[{idx}] Record: {row}")
        print("==========================================")
    else:
        print("[INFO] No 'wire_reconciliation' table found.")
        
    conn.close()

if __name__ == '__main__':
    view_wire_logs()

