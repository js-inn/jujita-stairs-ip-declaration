import sqlite3
import hmac
import hashlib
from datetime import datetime

DB_NAME = "financial_pipeline.db"
SECRET_KEY = b"jujita_secret_root_key"

def setup_russian_intelligence():
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
    
    # Russian defense and intelligence hierarchy mappings
    rus_mappings = [
        ("Government of the Russian Federation", "Ministry of Defense of the Russian Federation", "Federal Executive Ministry", "Russian Federation", datetime.now().isoformat()),
        ("Ministry of Defense of the Russian Federation", "General Staff of the Armed Forces of the Russian Federation", "Military Command Body", "Russian Federation", datetime.now().isoformat()),
        ("General Staff of the Armed Forces of the Russian Federation", "Main Directorate of the General Staff (GRU / GU)", "Foreign Military Intelligence Agency", "Russian Federation", datetime.now().isoformat())
    ]
    
    for parent, child, rel_type, juris, timestamp in rus_mappings:
        payload = f"{parent}:{child}:{rel_type}:{juris}".encode('utf-8')
        anchor = hmac.new(SECRET_KEY, payload, hashlib.sha256).hexdigest()
        
        cursor.execute('''
            INSERT INTO corporate_hierarchy (parent_entity, child_entity, relationship_type, jurisdiction, timestamp, hierarchy_anchor)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (parent, child, rel_type, juris, timestamp, anchor))
        
    conn.commit()
    
    # Query and display Russian defense institutional records
    cursor.execute("SELECT parent_entity, child_entity, relationship_type, jurisdiction FROM corporate_hierarchy WHERE parent_entity LIKE '%Russian Federation%' OR child_entity LIKE '%GRU%'")
    rows = cursor.fetchall()
    conn.close()
    
    print(f"\n=======================================================================")
    print(f"[*] RUSSIAN DEFENSE & INTELLIGENCE HIERARCHY MAPPED")
    print(f"=======================================================================\n")
    
    for parent, child, rel, juris in rows:
        print(f"Parent : {parent}")
        print(f" └── Child : {child} ({rel}) [{juris}]")
        print("-" * 65)

if __name__ == "__main__":
    setup_russian_intelligence()
