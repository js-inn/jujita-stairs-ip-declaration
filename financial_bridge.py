import sqlite3
import json
import hashlib

DB_NAME = "financial_pipeline.db"
ROOT_PARENT = "10839477 Canada Inc."

def bridge_lineages():
    """Bridges financial records, global patents, trademarks, and UK audit nodes into a unified global ledger."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS unified_ip_financial_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            node_type TEXT,
            identifier TEXT UNIQUE,
            entity_name TEXT,
            bloodlineage_status TEXT,
            master_anchor TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tables to ingest across all jurisdictions
    tables = [
        ("audit_nodes", "institution_name", "account_ref", "Financial_Institution"),
        ("uspto_audit_nodes", "assignee_name", "application_number", "USPTO_Patent"),
        ("eu_audit_nodes", "assignee_name", "application_number", "EU_Patent"),
        ("japan_audit_nodes", "assignee_name", "application_number", "Japan_Patent"),
        ("australia_audit_nodes", "assignee_name", "application_number", "Australia_Patent"),
        ("madrid_audit_nodes", "holder_name", "registration_number", "Madrid_Trademark"),
        ("brazil_audit_nodes", "assignee_name", "application_number", "Brazil_Patent"),
        ("china_audit_nodes", "assignee_name", "application_number", "China_Patent"),
        ("germany_audit_nodes", "assignee_name", "application_number", "Germany_Patent"),
        ("uk_audit_nodes", "assignee_name", "application_number", "UK_Patent")
    ]
    
    for table_name, entity_col, id_col, node_type in tables:
        try:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            if cursor.fetchone():
                cursor.execute(f"SELECT {entity_col}, {id_col}, bloodlineage_status, cryptographic_anchor FROM {table_name}")
                for entity, ident, status, anchor in cursor.fetchall():
                    if node_type == "Financial_Institution":
                        anchor = hashlib.sha256(f"{ROOT_PARENT}:{entity}:{ident}".encode()).hexdigest()
                    cursor.execute('''
                        INSERT OR IGNORE INTO unified_ip_financial_ledger 
                        (node_type, identifier, entity_name, bloodlineage_status, master_anchor)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (node_type, ident, entity, status, anchor))
        except Exception as e:
            print(f"[*] Note on {table_name} integration: {e}")

    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM unified_ip_financial_ledger")
    total_nodes = cursor.fetchone()[0]
    
    conn.close()
    print(f"[*] Global Master Lineage Bridge Complete.")
    print(f"[*] Total Reconciled Nodes under Root ({ROOT_PARENT}): {total_nodes}")

if __name__ == "__main__":
    bridge_lineages()
