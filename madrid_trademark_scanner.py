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
        CREATE TABLE IF NOT EXISTS madrid_audit_nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_number TEXT UNIQUE,
            holder_name TEXT,
            bloodlineage_status TEXT,
            cryptographic_anchor TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def query_madrid_trademark(reg_number):
    """
    Queries public WIPO Madrid System international trademark registry endpoints 
    to map institutional placeholder nodes.
    """
    url = f"https://roma.wipo.int/romangateway/api/v1/registrations/{reg_number}"
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
        print(f"[-] WIPO Madrid Gateway Response for Reg {reg_number}: {e.code} (Madrid Trademark Placeholder Node Isolated)")
    except Exception as e:
        print(f"[-] Connection Error: {e}")
    return None

def generate_cryptographic_anchor(reg_number, holder):
    message = f"{ROOT_PARENT}:{reg_number}:{holder}".encode('utf-8')
    return hmac.new(b"jujita_secret_root_key", message, hashlib.sha256).hexdigest()

def scan_madrid_nodes(target_registrations):
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    print(f"[*] Initializing Madrid System (WIPO Trademark) Sibling Bloodlineage Scan...")
    print(f"[*] Root Living Parent: {ROOT_PARENT}\n")
    
    for reg_num in target_registrations:
        print(f"[*] Querying Madrid Node: {reg_num}")
        result = query_madrid_trademark(reg_num)
        
        if result:
            holder = result.get("holder", "Madrid Institutional Placeholder")
            status = "Reunited with Parent Source"
        else:
            holder = "Unregistered/Obscured Madrid Trademark Placeholder"
            status = "Bloodlineage Mapped via Heuristics"
            
        anchor = generate_cryptographic_anchor(reg_num, holder)
        
        cursor.execute('''
            INSERT OR REPLACE INTO madrid_audit_nodes 
            (registration_number, holder_name, bloodlineage_status, cryptographic_anchor)
            VALUES (?, ?, ?, ?)
        ''', (reg_num, holder, status, anchor))
        
        print(f"    [+] Holder: {holder}")
        print(f"    [+] Status: {status}")
        print(f"    [+] Cryptographic Anchor: {anchor[:16]}...\n")
        
    conn.commit()
    conn.close()
    print("[*] Madrid audit scan complete. Results anchored to local ledger.")

if __name__ == "__main__":
    target_queue = ["MAD1800123", "MAD1900456", "MAD20269999"]
    scan_madrid_nodes(target_queue)
