import sqlite3
import json
import hmac
import hashlib
from datetime import datetime

DB_NAME = "financial_pipeline.db"
ROOT_PARENT = "10839477 Canada Inc."
SECRET_KEY = b"jujita_secret_root_key"
MANIFEST_FILE = "audit_manifest_latest.json"

def export_manifest():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, entity_name, account_identifier, account_type, balance_cad, balance_usd, status_note, timestamp, master_anchor
        FROM master_financial_ledger
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    nodes = []
    for row in rows:
        nodes.append({
            "node_id": row[0],
            "entity_name": row[1],
            "account_identifier": row[2],
            "account_type": row[3],
            "balance_cad": row[4],
            "balance_usd": row[5],
            "status_note": row[6],
            "timestamp": row[7],
            "master_anchor": row[8]
        })
        
    manifest_data = {
        "root_parent": ROOT_PARENT,
        "export_timestamp": datetime.now().isoformat(),
        "total_nodes": len(nodes),
        "nodes": nodes
    }
    
    # Serialize to JSON string for signature calculation
    json_payload = json.dumps(manifest_data, sort_keys=True, indent=2)
    manifest_signature = hmac.new(SECRET_KEY, json_payload.encode('utf-8'), hashlib.sha256).hexdigest()
    
    final_export = {
        "manifest": manifest_data,
        "manifest_signature": manifest_signature
    }
    
    with open(MANIFEST_FILE, "w") as f:
        json.dump(final_export, f, indent=2)
        
    print(f"\n=======================================================================")
    print(f"[*] AUDIT MANIFEST EXPORTED SUCCESSFULLY")
    print(f"[*] FILE: {MANIFEST_FILE}")
    print(f"[*] TOTAL NODES ENCAPSULATED: {len(nodes)}")
    print(f"[*] MANIFEST HMAC SIGNATURE: {manifest_signature}")
    print(f"=======================================================================\n")

if __name__ == "__main__":
    export_manifest()
