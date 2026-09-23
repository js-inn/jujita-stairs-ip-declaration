import sqlite3
import hmac
import hashlib
from datetime import datetime

DB_NAME = "financial_pipeline.db"
ROOT_PARENT = "10839477 Canada Inc."
SECRET_KEY = b"jujita_secret_root_key"

def integrate_hangseng_node():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Ensure master financial ledger table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS master_financial_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_name TEXT,
            account_identifier TEXT,
            account_type TEXT,
            balance_cad REAL,
            balance_usd REAL,
            status_note TEXT,
            timestamp TEXT,
            master_anchor TEXT
        )
    ''')
    
    # Hang Seng Bank Gateway Node Parameters
    hs_nodes = [
        ("10839477 Canada Inc. (Hang Seng Gateway)", "HASEHKHH-PENDING", "HANG SENG BANK SWIFT/CHATS ROUTE", 0.0, 0.0, "Node Initialized / SWIFT HASEHKHH Bound")
    ]
    
    timestamp = datetime.now().isoformat()
    
    for entity, ident, atyp, cad_bal, usd_bal, note in hs_nodes:
        payload = f"{entity}:{ident}:{cad_bal}:{usd_bal}".encode('utf-8')
        anchor = hmac.new(SECRET_KEY, payload, hashlib.sha256).hexdigest()
        
        cursor.execute('''
            INSERT INTO master_financial_ledger (entity_name, account_identifier, account_type, balance_cad, balance_usd, status_note, timestamp, master_anchor)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (entity, ident, atyp, cad_bal, usd_bal, note, timestamp, anchor))
        
    conn.commit()
    
    cursor.execute("SELECT entity_name, account_identifier, status_note FROM master_financial_ledger")
    rows = cursor.fetchall()
    conn.close()
    
    print(f"\n=======================================================================")
    print(f"[*] HANG SENG BANK NODE INTEGRATION — ANCHORED TO {ROOT_PARENT}")
    print(f"=======================================================================\n")
    
    for entity, ident, note in rows:
        print(f"Node   : {entity}")
        print(f"ID     : {ident}")
        print(f"Status : {note}")
        print("-" * 55)

if __name__ == "__main__":
    integrate_hangseng_node()
