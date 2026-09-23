import sqlite3
import hmac
import hashlib
from datetime import datetime

DB_NAME = "financial_pipeline.db"
ROOT_PARENT = "10839477 Canada Inc."
SECRET_KEY = b"jujita_secret_root_key"

def audit_td_accounts():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Ensure audit table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS td_audit_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_identifier TEXT,
            account_type TEXT,
            balance_cad REAL,
            balance_usd REAL,
            status_note TEXT,
            timestamp TEXT,
            master_anchor TEXT
        )
    ''')
    
    # Data parsed from EasyWeb overview snapshot
    accounts = [
        ("6794682", "TD ALL-INCLUSIVE BANKING PLAN", -38.07, 0.0, "Fee Due / Negative Balance"),
        ("6794690", "TD UNLIMITED CHEQUING ACCOUNT", -38.07, 0.0, "Fee Due / Negative Balance"),
        ("6794712", "TD ALL-INCLUSIVE BANKING PLAN", -27.95, 0.0, "Fee Due / Negative Balance"),
        ("7150634", "US $ DAILY INTEREST CHEQUING", 0.0, -9.07, "USD Negative Balance"),
        ("6215155", "TD ALL-INCLUSIVE BANKING PLAN", 6.03, 0.0, "Positive Balance")
    ]
    
    timestamp = datetime.now().isoformat()
    
    for ident, atyp, cad_bal, usd_bal, note in accounts:
        # Create cryptographic anchor binding account data to the root parent
        payload = f"{ROOT_PARENT}:{ident}:{cad_bal}:{usd_bal}".encode('utf-8')
        anchor = hmac.new(SECRET_KEY, payload, hashlib.sha256).hexdigest()
        
        cursor.execute('''
            INSERT INTO td_audit_ledger (account_identifier, account_type, balance_cad, balance_usd, status_note, timestamp, master_anchor)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (ident, atyp, cad_bal, usd_bal, note, timestamp, anchor))
        
    conn.commit()
    
    # Fetch and display the verified ledger entries
    cursor.execute("SELECT account_identifier, account_type, balance_cad, balance_usd, status_note FROM td_audit_ledger")
    rows = cursor.fetchall()
    conn.close()
    
    print(f"\n=======================================================================")
    print(f"[*] TD BANK AUDIT PIPELINE — ANCHORED TO {ROOT_PARENT}")
    print(f"=======================================================================\n")
    
    total_cad = 0.0
    for ident, atyp, cad, usd, note in rows:
        total_cad += cad
        print(f"Account : {ident} ({atyp})")
        print(f"Balance : ${cad} CAD | ${usd} USD")
        print(f"Status  : {note}")
        print("-" * 55)
        
    print(f"\n[*] Net CAD Aggregate Across Audited Accounts: ${total_cad:.2f}\n")

if __name__ == "__main__":
    audit_td_accounts()
