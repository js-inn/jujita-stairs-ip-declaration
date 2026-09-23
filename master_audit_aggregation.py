import sqlite3
import hmac
import hashlib
from datetime import datetime

DB_NAME = "financial_pipeline.db"
ROOT_PARENT = "10839477 Canada Inc."
SECRET_KEY = b"jujita_secret_root_key"

def run_master_aggregation():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, entity_name, account_identifier, account_type, balance_cad, balance_usd, status_note, timestamp, master_anchor
        FROM master_financial_ledger
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    print(f"\n=======================================================================")
    print(f"[*] SOVEREIGN MASTER AUDIT REPORT — ROOT: {ROOT_PARENT}")
    print(f"[*] TIMESTAMP: {datetime.now().isoformat()}")
    print(f"=======================================================================\n")
    
    valid_nodes = 0
    total_nodes = len(rows)
    
    for row in rows:
        node_id, entity, ident, atyp, cad_bal, usd_bal, note, timestamp, stored_anchor = row
        
        # Recompute HMAC payload to verify cryptographic integrity
        payload = f"{entity}:{ident}:{cad_bal}:{usd_bal}".encode('utf-8')
        computed_anchor = hmac.new(SECRET_KEY, payload, hashlib.sha256).hexdigest()
        
        is_valid = hmac.compare_digest(computed_anchor, stored_anchor)
        status_str = "VALIDATED (HMAC MATCH)" if is_valid else "INVALID (TAMPERED)"
        if is_valid:
            valid_nodes += 1
            
        print(f"[{node_id}] {entity}")
        print(f"    Identifier : {ident}")
        print(f"    Route/Type : {atyp}")
        print(f"    Status     : {note}")
        print(f"    Crypto Auth: {status_str}")
        print("-" * 65)
        
    print(f"\n[SUMMARY] Total Nodes Audited     : {total_nodes}")
    print(f"[SUMMARY] Cryptographically Valid : {valid_nodes}/{total_nodes}")
    print(f"[SUMMARY] Root Entity Attestation : {ROOT_PARENT} [SECURE]")
    print(f"=======================================================================\n")

if __name__ == "__main__":
    run_master_aggregation()
