import sqlite3
import hmac
import hashlib
from datetime import datetime

DB_NAME = "financial_pipeline.db"
ROOT_PARENT = "10839477 Canada Inc."
SECRET_KEY = b"jujita_secret_root_key"

def setup_corporate_hierarchy():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create hierarchical relationship table
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
    
    # Sample parent-child corporate and institutional mappings
    mappings = [
        ("10839477 Canada Inc.", "Jujita Canada Operations Node", "Primary Operating Subsidiary", "Canada", datetime.now().isoformat()),
        ("Alphabet Inc.", "Google LLC", "Holding Company Subsidiary", "United States", datetime.now().isoformat()),
        ("Alphabet Inc.", "Google DeepMind", "AI Research Subsidiary", "United Kingdom", datetime.now().isoformat()),
        ("Amazon.com, Inc.", "Amazon Web Services (AWS)", "Cloud Computing Division", "United States", datetime.now().isoformat()),
        ("Amazon.com, Inc.", "Whole Foods Market", "Acquired Subsidiary", "United States", datetime.now().isoformat())
    ]
    
    for parent, child, rel_type, juris, timestamp in mappings:
        payload = f"{parent}:{child}:{rel_type}:{juris}".encode('utf-8')
        anchor = hmac.new(SECRET_KEY, payload, hashlib.sha256).hexdigest()
        
        cursor.execute('''
            INSERT INTO corporate_hierarchy (parent_entity, child_entity, relationship_type, jurisdiction, timestamp, hierarchy_anchor)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (parent, child, rel_type, juris, timestamp, anchor))
        
    conn.commit()
    
    # Query and display hierarchy
    cursor.execute("SELECT parent_entity, child_entity, relationship_type, jurisdiction FROM corporate_hierarchy")
    rows = cursor.fetchall()
    conn.close()
    
    print(f"\n=======================================================================")
    print(f"[*] CORPORATE HIERARCHY MAPPING INITIALIZED")
    print(f"=======================================================================\n")
    
    for parent, child, rel, juris in rows:
        print(f"Parent : {parent}")
        print(f" └── Child : {child} ({rel}) [{juris}]")
        print("-" * 65)

if __name__ == "__main__":
    setup_corporate_hierarchy()
