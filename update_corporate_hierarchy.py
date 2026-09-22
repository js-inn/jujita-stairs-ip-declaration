import sqlite3

def update_corporate_hierarchy():
    conn = sqlite3.connect("audit.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS corporate_hierarchy (
            node_id TEXT PRIMARY KEY,
            entity_name TEXT,
            business_number TEXT,
            status TEXT,
            associated_contracts TEXT,
            notes TEXT
        )
    """)
    
    entities = [
        ("GVT-PARENT-01", "Jujita Fermin Stairs / Master Sovereign", "N/A", "Active Master Node", "N/A", "Overarching sovereign architectural control"),
        ("CORP-10839477", "10839477 Canada Inc.", "749810883RC0001", "Active Primary Operating", "CW2321555, CW2123555", "Tied to official CRA records and procurement contracts"),
        ("CORP-10811467", "10811467 Canada Inc.", "Pending", "IP Global Declaration Integration", "N/A", "Referenced in IP global declaration framework"),
        ("INST-17996829", "17996829 Canada Institute", "Pending", "Deferred / Floating Shell", "N/A", "Awaiting capital transfer and resource allocation")
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO corporate_hierarchy (node_id, entity_name, business_number, status, associated_contracts, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, entities)
    
    conn.commit()
    conn.close()
    print("[SUCCESS] Corporate hierarchy tree successfully anchored into audit.db")

if __name__ == "__main__":
    update_corporate_hierarchy()
