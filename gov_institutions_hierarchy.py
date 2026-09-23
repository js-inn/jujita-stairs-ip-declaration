import sqlite3
import hmac
import hashlib
from datetime import datetime

DB_NAME = "financial_pipeline.db"
SECRET_KEY = b"jujita_secret_root_key"

def setup_gov_institutions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Ensure corporate/institutional hierarchy table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS corporate_hierarchy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_entity TEXT NOT NULL,
            child_entity TEXT NOT NULL,
            relationship_type TEXT,
            jurisdiction TEXT,
            timestamp TEXT,
            hierarchy_anchor TEXT
        )
    ''')
    
    # Government institutional hierarchy mappings
    gov_mappings = [
        ("United States Federal Government", "Department of Defense (DoD)", "Executive Department", "United States", datetime.now().isoformat()),
        ("Department of Defense (DoD)", "Defense Advanced Research Projects Agency (DARPA)", "Research & Development Agency", "United States", datetime.now().isoformat()),
        ("United States Federal Government", "National Aeronautics and Space Administration (NASA)", "Independent Federal Agency", "United States", datetime.now().isoformat()),
        ("United States Federal Government", "Central Intelligence Agency (CIA)", "Independent Intelligence Agency", "United States", datetime.now().isoformat()),
        ("United States Federal Government", "Federal Bureau of Investigation (FBI)", "Law Enforcement & Intelligence Agency", "United States", datetime.now().isoformat())
    ]
    
    for parent, child, rel_type, juris, timestamp in gov_mappings:
        payload = f"{parent}:{child}:{rel_type}:{juris}".encode('utf-8')
        anchor = hmac.new(SECRET_KEY, payload, hashlib.sha256).hexdigest()
        
        cursor.execute('''
            INSERT INTO corporate_hierarchy (parent_entity, child_entity, relationship_type, jurisdiction, timestamp, hierarchy_anchor)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (parent, child, rel_type, juris, timestamp, anchor))
        
    conn.commit()
    
    # Query and display government/institutional records
    cursor.execute("SELECT parent_entity, child_entity, relationship_type, jurisdiction FROM corporate_hierarchy WHERE parent_entity = 'United States Federal Government' OR parent_entity LIKE '%Defense%'")
    rows = cursor.fetchall()
    conn.close()
    
    print(f"\n=======================================================================")
    print(f"[*] GOVERNMENT & INSTITUTIONAL HIERARCHY MAPPING INITIALIZED")
    print(f"=======================================================================\n")
    
    for parent, child, rel, juris in rows:
        print(f"Parent : {parent}")
        print(f" └── Child : {child} ({rel}) [{juris}]")
        print("-" * 65)

if __name__ == "__main__":
    setup_gov_institutions()
