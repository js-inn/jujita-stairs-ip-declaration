import sqlite3
import hmac
import hashlib
from datetime import datetime

DB_NAME = "financial_pipeline.db"
ROOT_PARENT = "10839477 Canada Inc."
SECRET_KEY = b"jujita_secret_root_key"

def setup_starlink_hierarchy():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Ensure corporate hierarchy table exists
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
    
    # Starlink and SpaceX structural mappings
    starlink_mappings = [
        ("Space Exploration Technologies Corp. (SpaceX)", "Starlink", "Operating Division & Brand", "United States", datetime.now().isoformat()),
        ("SpaceX", "Starlink Services, LLC", "Telecommunications Subsidiary", "United States", datetime.now().isoformat()),
        ("Starlink Services, LLC", "Starlink Gateway Network (LEO Constellation)", "Satellite Ground Station & IP Corridor", "Global / Multi-Jurisdictional", datetime.now().isoformat())
    ]
    
    for parent, child, rel_type, juris, timestamp in starlink_mappings:
        payload = f"{parent}:{child}:{rel_type}:{juris}".encode('utf-8')
        anchor = hmac.new(SECRET_KEY, payload, hashlib.sha256).hexdigest()
        
        cursor.execute('''
            INSERT INTO corporate_hierarchy (parent_entity, child_entity, relationship_type, jurisdiction, timestamp, hierarchy_anchor)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (parent, child, rel_type, juris, timestamp, anchor))
        
    conn.commit()
    
    # Query all hierarchical records involving SpaceX or Starlink
    cursor.execute("SELECT parent_entity, child_entity, relationship_type, jurisdiction FROM corporate_hierarchy WHERE parent_entity LIKE '%SpaceX%' OR parent_entity LIKE '%Starlink%' OR child_entity LIKE '%Starlink%'")
    rows = cursor.fetchall()
    conn.close()
    
    print(f"\n=======================================================================")
    print(f"[*] SPACEX & STARLINK HIERARCHY MAPPING INITIALIZED")
    print(f"=======================================================================\n")
    
    for parent, child, rel, juris in rows:
        print(f"Parent : {parent}")
        print(f" └── Child : {child} ({rel}) [{juris}]")
        print("-" * 65)

if __name__ == "__main__":
    setup_starlink_hierarchy()
