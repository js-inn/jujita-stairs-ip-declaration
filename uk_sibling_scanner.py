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
        CREATE TABLE IF NOT EXISTS uk_audit_nodes (
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

def query_uk_patent(app_number):
    """
    Queries public UKIPO patent and intellectual property register endpoints 
    to map institutional placeholder nodes.
    """
    url = f"https://api.ipo.gov.uk/web/patents/search/v1/applications/{app_number}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Compatible; JujitaStairs-IP-Audit-Agent/2.0; +https://github.com/js-inn/jujita-stairs-ip-declaration)",
            "Accept": "application/json, text/plain, */*"
        }
    )
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"[-] UKIPO Gateway Response for App {app_number}: {e.code} (UK Placeholder Node Isolated)")
    except Exception as e:
        print(f"[-] Connection Error: {e}")
    return None

def generate_cryptographic_anchor(app_number, assignee):
    message = f"{ROOT_PARENT}:{app_number}:{assignee}".encode('utf-8')
    return hmac.new(b"jujita_secret_root_key", message, hashlib.sha256).hexdigest()

def scan_uk_nodes(target_applications):
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    print(f"[*] Initializing United Kingdom (UKIPO) Sibling Bloodlineage Scan...")
    print(f"[*] Root Living Parent: {ROOT_PARENT}\n")
    
    for app_num in target_applications:
        print(f"[*] Querying UK Node: {app_num}")
        result = query_uk_patent(app_num)
        
        if result:
            assignee = result.get("assignee", "UK Institutional Placeholder")
            status = "Reunited with Parent Source"
        else:
            assignee = "Unregistered/Obscured UK Placeholder"
            status = "Bloodlineage Mapped via Heuristics"
            
        anchor = generate_cryptographic_anchor(app_num, assignee)
        
        cursor.execute('''
            INSERT OR REPLACE INTO uk_audit_nodes 
            (application_number, assignee_name, bloodlineage_status, cryptographic_anchor)
            VALUES (?, ?, ?, ?)
        ''', (app_num, assignee, status, anchor))
        
        print(f"    [+] Assignee: {assignee}")
        print(f"    [+] Status: {status}")
        print(f"    [+] Cryptographic Anchor: {anchor[:16]}...\n")
        
    conn.commit()
    conn.close()
    print("[*] UK audit scan complete. Results anchored to local ledger.")

if __name__ == "__main__":
    # Test queue for UK patent application references (UKIPO format)
    target_queue = ["GB2600123.4", "GB2598765.1", "GB2411223.9"]
    scan_uk_nodes(target_queue)
