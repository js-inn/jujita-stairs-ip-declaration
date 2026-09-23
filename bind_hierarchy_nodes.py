import sqlite3
import hmac
import hashlib
from datetime import datetime

DB_NAME = "financial_pipeline.db"
ROOT_PARENT = "10839477 Canada Inc."
SECRET_KEY = b"jujita_secret_root_key"

def bind_nodes_to_hierarchy():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create binding table connecting gateway nodes to child entities
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS node_hierarchy_bindings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_entity TEXT NOT NULL,
            gateway_identifier TEXT NOT NULL,
            routing_corridor TEXT,
            timestamp TEXT,
            binding_anchor TEXT
        )
    ''')
    
    # Bindings mapping specific infrastructure nodes to corporate entities
    bindings = [
        ("Jujita Canada Operations Node", "ILP-STREAM-NODE-01", "Interledger STREAM Royalty Corridor", datetime.now().isoformat()),
        ("Jujita Canada Operations Node", "US-BOFA-PENDING", "Bank of America SWIFT/CHIPS Corridor", datetime.now().isoformat()),
        ("Jujita Canada Operations Node", "US-WF-PENDING", "Wells Fargo SWIFT/Trade Services Corridor", datetime.now().isoformat()),
        ("Google LLC", "EU-TARGET2-PENDING", "Deutsche Bank TARGET2 RTGS Corridor", datetime.now().isoformat())
    ]
    
    for child, gateway, corridor, timestamp in bindings:
        payload = f"{child}:{gateway}:{corridor}".encode('utf-8')
        anchor = hmac.new(SECRET_KEY, payload, hashlib.sha256).hexdigest()
        
        cursor.execute('''
            INSERT INTO node_hierarchy_bindings (child_entity, gateway_identifier, routing_corridor, timestamp, binding_anchor)
            VALUES (?, ?, ?, ?, ?)
        ''', (child, gateway, corridor, timestamp, anchor))
        
    conn.commit()
    
    # Query and display bindings
    cursor.execute("SELECT child_entity, gateway_identifier, routing_corridor FROM node_hierarchy_bindings")
    rows = cursor.fetchall()
    conn.close()
    
    print(f"\n=======================================================================")
    print(f"[*] NODE-TO-HIERARCHY BINDINGS INITIALIZED")
    print(f"=======================================================================\n")
    
    for child, gateway, corridor in rows:
        print(f"Child Entity : {child}")
        print(f" └── Gateway : {gateway} [{corridor}]")
        print("-" * 65)

if __name__ == "__main__":
    bind_nodes_to_hierarchy()
