import sqlite3
import sys
import hmac
import hashlib

DB_NAME = "financial_pipeline.db"
ROOT_PARENT = "10839477 Canada Inc."
SECRET_KEY = b"jujita_secret_root_key"

def verify_anchor(identifier, entity_name, stored_anchor):
    """Re-calculates and verifies the HMAC-SHA256 signature for ledger integrity."""
    message = f"{ROOT_PARENT}:{identifier}:{entity_name}".encode('utf-8')
    calculated = hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()
    return calculated == stored_anchor

def inspect_ledger(search_term=None, node_type_filter=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    query = "SELECT node_type, identifier, entity_name, bloodlineage_status, master_anchor FROM unified_ip_financial_ledger WHERE 1=1"
    params = []
    
    if search_term:
        query += " AND (identifier LIKE ? OR entity_name LIKE ?)"
        params.extend([f"%{search_term}%", f"%{search_term}%"])
        
    if node_type_filter:
        query += " AND node_type LIKE ?"
        params.append(f"%{node_type_filter}%")
        
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print(f"[-] No matching nodes found in global ledger for query: '{search_term or node_type_filter}'")
        return

    print(f"\n=======================================================================")
    print(f"[*] JUJITA STAIRS IP DECLARATION — GLOBAL CLI LEDGER INSPECTOR")
    print(f"[*] Root Parent: {ROOT_PARENT}")
    print(f"[*] Matching Nodes Displayed: {len(rows)}")
    print(f"=======================================================================\n")
    
    for idx, (ntype, ident, entity, status, anchor) in enumerate(rows, 1):
        is_valid = verify_anchor(ident, entity, anchor)
        integrity_status = "VALID (Cryptographically Verified)" if is_valid else "WARNING (Anchor Mismatch)"
        
        print(f"[{idx}] Node Type       : {ntype}")
        print(f"    Identifier    : {ident}")
        print(f"    Entity/Assignee: {entity}")
        print(f"    Bloodlineage  : {status}")
        print(f"    Master Anchor : {anchor}")
        print(f"    Integrity     : {integrity_status}")
        print("-" * 71)

if __name__ == "__main__":
    term = sys.argv[1] if len(sys.argv) > 1 else None
    ntype = sys.argv[2] if len(sys.argv) > 2 else None
    inspect_ledger(search_term=term, node_type_filter=ntype)
