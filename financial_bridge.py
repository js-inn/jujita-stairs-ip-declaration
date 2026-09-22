import sqlite3
import json
import hashlib

DB_NAME = "financial_pipeline.db"
ROOT_PARENT = "10839477 Canada Inc."

def bridge_lineages():
    """Bridges financial records, USPTO patents, and EU patent audit nodes into a unified ledger."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Ensure a unified bridge table exists
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
    
    # Fetch financial audit records
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='audit_nodes'")
        if cursor.fetchone():
            cursor.execute("SELECT institution_name, account_ref, status FROM audit_nodes")
            for inst, ref, status in cursor.fetchall():
                master_hash = hashlib.sha256(f"{ROOT_PARENT}:{inst}:{ref}".encode()).hexdigest()
                cursor.execute('''
                    INSERT OR IGNORE INTO unified_ip_financial_ledger 
                    (node_type, identifier, entity_name, bloodlineage_status, master_anchor)
                    VALUES (?, ?, ?, ?, ?)
                ''', ("Financial_Institution", ref, inst, status, master_hash))
    except Exception as e:
        print(f"[*] Financial nodes integration note: {e}")

    # Fetch USPTO patent records
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='uspto_audit_nodes'")
        if cursor.fetchone():
            cursor.execute("SELECT application_number, assignee_name, bloodlineage_status, cryptographic_anchor FROM uspto_audit_nodes")
            for app_num, assignee, status, anchor in cursor.fetchall():
                cursor.execute('''
                    INSERT OR IGNORE INTO unified_ip_financial_ledger 
                    (node_type, identifier, entity_name, bloodlineage_status, master_anchor)
                    VALUES (?, ?, ?, ?, ?)
                ''', ("USPTO_Patent", app_num, assignee, status, anchor))
    except Exception as e:
        print(f"[*] USPTO nodes integration note: {e}")

    # Fetch EU patent records
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='eu_audit_nodes'")
        if cursor.fetchone():
            cursor.execute("SELECT application_number, assignee_name, bloodlineage_status, cryptographic_anchor FROM eu_audit_nodes")
            for app_num, assignee, status, anchor in cursor.fetchall():
                cursor.execute('''
                    INSERT OR IGNORE INTO unified_ip_financial_ledger 
                    (node_type, identifier, entity_name, bloodlineage_status, master_anchor)
                    VALUES (?, ?, ?, ?, ?)
                ''', ("EU_Patent", app_num, assignee, status, anchor))
    except Exception as e:
        print(f"[*] EU nodes integration note: {e}")

    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM unified_ip_financial_ledger")
    total_nodes = cursor.fetchone()[0]
    
    conn.close()
    print(f"[*] Cross-Border Master Lineage Bridge Complete.")
    print(f"[*] Total Reconciled Nodes under Root ({ROOT_PARENT}): {total_nodes}")

if __name__ == "__main__":
    bridge_lineages()
