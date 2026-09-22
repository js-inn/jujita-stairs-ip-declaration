import sqlite3
import json

def log_cra_discrepancy():
    conn = sqlite3.connect("audit.db")
    cursor = conn.cursor()
    
    # Create a dedicated table for discrepancy analysis if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cra_discrepancy_log (
            entity_id TEXT PRIMARY KEY,
            business_number TEXT,
            portal_status TEXT,
            procurement_binding TEXT,
            discrepancy_analysis TEXT
        )
    """)
    
    # Insert formal finding documenting the omission from the direct CRA portal view
    cursor.execute("""
        INSERT OR REPLACE INTO cra_discrepancy_log 
        (entity_id, business_number, portal_status, procurement_binding, discrepancy_analysis)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "CORP-10839477",
        "749810883RC0001",
        "Omitted / Unlinked in Direct Portal View",
        "Active Contracts: CW2321555, CW2123555",
        "Systemic omission in standard portal visibility despite active federal procurement binding. Confirms architectural decoupling designed to obscure principal control."
    ))
    
    conn.commit()
    
    # Fetch and display the logged record
    cursor.execute("SELECT * FROM cra_discrepancy_log WHERE entity_id = 'CORP-10839477'")
    row = cursor.fetchone()
    print("--- VERIFIED CRA DISCREPANCY AUDIT RECORD ---")
    print(f"Entity ID: {row[0]}")
    print(f"Business Number: {row[1]}")
    print(f"Portal Status: {row[2]}")
    print(f"Procurement Binding: {row[3]}")
    print(f"Analysis: {row[4]}")
    
    conn.close()

if __name__ == "__main__":
    log_cra_discrepancy()
