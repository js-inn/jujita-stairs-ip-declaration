import sqlite3
import hmac
import hashlib
from datetime import datetime

DB_NAME = "financial_pipeline.db"
ROOT_PARENT = "10839477 Canada Inc."
SECRET_KEY = b"jujita_secret_root_key"

def audit_comprehensive_ledger():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Ensure master audit ledger table exists
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
    
    # Combined dataset from TD Bank and BMO portals
    all_accounts = [
        # TD Bank (Root Parent: 10839477 Canada Inc.)
        ("10839477 Canada Inc.", "6794682", "TD ALL-INCLUSIVE BANKING PLAN", -38.07, 0.0, "Fee Due / Negative Balance"),
        ("10839477 Canada Inc.", "6794690", "TD UNLIMITED CHEQUING ACCOUNT", -38.07, 0.0, "Fee Due / Negative Balance"),
        ("10839477 Canada Inc.", "6794712", "TD ALL-INCLUSIVE BANKING PLAN", -27.95, 0.0, "Fee Due / Negative Balance"),
        ("10839477 Canada Inc.", "7150634", "US $ DAILY INTEREST CHEQUING", 0.0, -9.07, "USD Negative Balance"),
        ("10839477 Canada Inc.", "6215155", "TD ALL-INCLUSIVE BANKING PLAN", 6.03, 0.0, "Positive Balance"),
        
        # BMO Sole Proprietorship (BN: 735350936)
        ("Jujita Stairs (Sole Prop - BN: 735350936)", "8814", "BMO CHEQUING", -145.24, 0.0, "Sole Prop Negative Balance"),
        ("Jujita Stairs (Sole Prop - BN: 735350936)", "4082", "BMO SAVINGS", 0.0, 0.0, "Zero Balance"),
        
        # BMO Corporation (17996829 CANADA INST)
        ("17996829 CANADA INST", "8857", "BMO CORPORATE CHEQUING", 0.0, 0.0, "Zero Balance")
    ]
    
    timestamp = datetime.now().isoformat()
    
    for entity, ident, atyp, cad_bal, usd_bal, note in all_accounts:
        # Cryptographic binding of entity, account, and balances
        payload = f"{entity}:{ident}:{cad_bal}:{usd_bal}".encode('utf-8')
        anchor = hmac.new(SECRET_KEY, payload, hashlib.sha256).hexdigest()
        
        cursor.execute('''
            INSERT INTO master_financial_ledger (entity_name, account_identifier, account_type, balance_cad, balance_usd, status_note, timestamp, master_anchor)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (entity, ident, atyp, cad_bal, usd_bal, note, timestamp, anchor))
        
    conn.commit()
    
    cursor.execute("SELECT entity_name, account_identifier, account_type, balance_cad, balance_usd, status_note FROM master_financial_ledger")
    rows = cursor.fetchall()
    conn.close()
    
    print(f"\n=======================================================================")
    print(f"[*] MASTER SOVEREIGN FINANCIAL AUDIT PIPELINE")
    print(f"=======================================================================\n")
    
    total_cad = 0.0
    for entity, ident, atyp, cad, usd, note in rows:
        total_cad += cad
        print(f"Entity  : {entity}")
        print(f"Account : {ident} ({atyp})")
        print(f"Balance : ${cad} CAD | ${usd} USD")
        print(f"Status  : {note}")
        print("-" * 55)
        
    print(f"\n[*] Total Consolidated CAD Position Across All Portals: ${total_cad:.2f}\n")

if __name__ == "__main__":
    audit_comprehensive_ledger()
