import sqlite3
import hmac
import hashlib
from datetime import datetime

DB_NAME = "financial_pipeline.db"
SECRET_KEY = b"jujita_secret_root_key"

def setup_ai_hierarchy():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create AI ecosystem hierarchy table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_ecosystem_hierarchy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_entity TEXT,
            child_entity TEXT,
            relationship_type TEXT,
            jurisdiction TEXT,
            timestamp TEXT,
            hierarchy_anchor TEXT
        )
    ''')
    
    ai_nodes = [
        ("Alphabet Inc.", "Google DeepMind", "Subsidiary Research Lab", "United States"),
        ("Meta Platforms, Inc.", "Meta AI (FAIR)", "Corporate Research Division", "United States"),
        ("Amazon.com, Inc.", "Anthropic", "Strategic Cloud Partner & Investor", "United States"),
        ("OpenAI Inc. (Nonprofit)", "OpenAI Global LLC", "Controlled Commercial Subsidiary", "United States"),
        ("Hugging Face Inc.", "Open-Source Community Ecosystem", "Platform Hub", "United States / France")
    ]
    
    for parent, child, rel, juris in ai_nodes:
        payload = f"{parent}:{child}:{rel}:{juris}".encode('utf-8')
        anchor = hmac.new(SECRET_KEY, payload, hashlib.sha256).hexdigest()
        
        cursor.execute('''
            INSERT INTO ai_ecosystem_hierarchy (parent_entity, child_entity, relationship_type, jurisdiction, timestamp, hierarchy_anchor)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (parent, child, rel, juris, datetime.now().isoformat(), anchor))
        
    conn.commit()
    
    # Query and display
    cursor.execute("SELECT parent_entity, child_entity, relationship_type, jurisdiction FROM ai_ecosystem_hierarchy")
    rows = cursor.fetchall()
    conn.close()
    
    print(f"\n=======================================================================")
    print(f"[*] AI ECOSYSTEM HIERARCHY MAPPED & ANCHORED ({len(rows)} nodes)")
    print(f"=======================================================================\n")
    
    for parent, child, rel, juris in rows:
        print(f"  [Parent] {parent}")
        print(f"   └── [AI Entity] {child} ({rel}) [{juris}]")
        print("-" * 65)

if __name__ == "__main__":
    setup_ai_hierarchy()
