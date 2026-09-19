import sqlite3
import os

DB_PATH = "/storage/emulated/0/Government_Contracts_Compliance/compliance_pipeline.db"
OUTPUT_PATH = "/storage/emulated/0/Government_Contracts_Compliance/Legal_Briefing_Package.txt"

def scan_and_update_package():
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Inspect all table schemas and contents for any numerical/value data
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    
    financial_data_summary = []
    
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [col[1] for col in cursor.fetchall()]
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        financial_data_summary.append(f"\nTable: {table} (Columns: {columns})")
        for row in rows:
            financial_data_summary.append(f"  Row: {row}")

    conn.close()

    # Append findings to the Legal Briefing Package
    append_text = f"""
--------------------------------------------------------------------------------
6. DETAILED LEDGER & TABLE DUMP (FINANCIAL & AUDIT RECORDS)
--------------------------------------------------------------------------------
The following are the raw data records extracted directly from the compliance 
pipeline database tables (trust_reconciliation and wire_reconciliation):
""" + "\n".join(financial_data_summary) + "\n================================================================================\n"

    # Read existing package content or create new
    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            content = f.read().strip()
        # Remove trailing border if present to append cleanly
        content = content.split("================================================================================")[0] + content
    else:
        content = ""

    # Append the financial dump
    with open(OUTPUT_PATH, "a", encoding="utf-8") as f:
        f.write(append_text)
        
    print(f"[SUCCESS] Updated legal briefing package with complete database records at:\n{OUTPUT_PATH}")

if __name__ == "__main__":
    scan_and_update_package()

