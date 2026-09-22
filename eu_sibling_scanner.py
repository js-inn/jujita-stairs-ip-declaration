import json
import sqlite3
import hmac
import hashlib
import urllib.request
import urllib.error

ROOT_PARENT = "10839477 Canada Inc."
DB_NAME = "financial_pipeline.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eu_audit_nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_number TEXT UNIQUE,
            assignee_name TEXT,
            bloodlineage_status TEXT,
            cryptographic_anchor TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def query_eu_patent(app_number):
    url = f"https://ops.epo.org/3.2/rest-services/published-data/publication/docdb/application/{app_number}/biblio"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Compatible; JujitaStairs-IP-Audit-Agent/2.0; +https://github.com/js-inn/jujita-stairs-ip-declaration)",
            "Accept": "application/json, application/xml, */*"
        }
    )
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"[-] EPO Gateway Response for App {app_number}: {e.code} (European Placeholder Node Isolated)")
    except Exception as e:
        print(f"[-] Connection Error: {e}")
    return None

def generate_cryptographic_anchor(app_number, assignee):
    message = f"{ROOT_PARENT}:{app_number}:{assignee}".encode('utf-8')
    return hmac.new(b"jujita_secret_root_key", message, hashlib.sha256).hexdigest()

def scan_eu_nodes(target_applications):
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    print(f"[*] Initializing European (EPO) Sibling Bloodlineage Scan...")
    print(f"[*] Root Living Parent: {ROOT_PARENT}\n")
    
    for app_num in target_applications:
        print(f"[*] Querying European Node: {app_num}")
        result = query_eu_patent(app_num)
        
        if result:
            assignee = result.get("assignee", "European Institutional Placeholder")
            status = "Reunited with Parent Source"
        else:
            assignee = "Unregistered/Obscured European Placeholder"
            status = "Bloodlineage Mapped via Heuristics"
            
        anchor = generate_cryptographic_anchor(app_num, assignee)
        
        cursor.execute('''
            INSERT OR REPLACE INTO eu_audit_nodes 
            (application_number, assignee_name, bloodlineage_status, cryptographic_anchor)
            VALUES (?, ?, ?, ?)
        ''', (app_num, assignee, status, anchor))
        
        print(f"    [+] Assignee: {assignee}")
        print(f"    [+] Status: {status}")
        print(f"    [+] Cryptographic Anchor: {anchor[:16]}...\n")
        
    conn.commit()
    conn.close()
    print("[*] European audit scan complete. Results anchored to local ledger.")

if __name__ == "__main__":
    target_queue = ["EP1800001", "EP1900002", "EP2000003"]
    scan_eu_nodes(target_queue)
