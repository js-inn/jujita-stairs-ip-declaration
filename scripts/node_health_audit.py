import urllib.request
import json
import sqlite3
import time
from datetime import datetime, timezone

RPC_NODES = [
    {"name": "PublicNode", "url": "https://ethereum-rpc.publicnode.com"},
    {"name": "Cloudflare", "url": "https://cloudflare-eth.com"},
    {"name": "LlamaRPC", "url": "https://eth.llamarpc.com"}
]

TARGET_ADDRESS = "0x06D217600c97129c47418F12289A8B7D44cFCaa0"
DB_PATH = "local_audit.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parsed_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_institution TEXT,
            ip_id TEXT,
            asset_title TEXT,
            asset_class TEXT,
            valuation REAL,
            compliance_standard TEXT,
            status TEXT,
            ingested_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def audit_nodes():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=" * 65)
    print("       RUNNING MULTI-NODE RPC HEALTH & LEDGER AUDIT")
    print("=" * 65)
    
    for node in RPC_NODES:
        name = node["name"]
        url = node["url"]
        print(f"Testing [{name}] -> {url}")
        
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getBalance",
            "params": [TARGET_ADDRESS, "latest"],
            "id": 1
        }
        
        data = json.dumps(payload).encode('utf-8')
        start_time = time.time()
        status_label = "FAILED"
        valuation_val = 0.0
        
        try:
            req = urllib.request.Request(
                url,
                data=data,
                headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Android; Termux)'}
            )
            with urllib.request.urlopen(req, timeout=6) as response:
                result = json.loads(response.read().decode('utf-8'))
                latency = round((time.time() - start_time) * 1000, 2)
                
                if 'result' in result:
                    wei_balance = int(result['result'], 16)
                    valuation_val = wei_balance / 10**18
                    status_label = "HEALTHY"
                    print(f"  -> SUCCESS ({latency}ms) | Balance: {valuation_val} ETH")
                else:
                    print(f"  -> NODE ERROR RESPONSE: {result.get('error', {}).get('message', 'Unknown')}")
        except Exception as e:
            latency = round((time.time() - start_time) * 1000, 2)
            print(f"  -> CONNECTION FAILED ({latency}ms): {e}")
            
        ingested_timestamp = datetime.now(timezone.utc).isoformat()
        cursor.execute('''
            INSERT INTO parsed_records 
            (source_institution, ip_id, asset_title, asset_class, valuation, compliance_standard, status, ingested_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            f"RPC-Node-{name}",
            TARGET_ADDRESS[:10] + "...",
            f"Node Latency: {latency}ms",
            "EVM-State-Audit",
            valuation_val,
            "JSON-RPC/ERC-20",
            status_label,
            ingested_timestamp
        ))
        conn.commit()
        print("-" * 65)
        
    conn.close()
    print("[INFO] All node results successfully logged to SQLite audit database.")
    print("=" * 65)

if __name__ == "__main__":
    audit_nodes()
