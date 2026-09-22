import os
import sqlite3
from datetime import datetime, timezone

DB_PATH = "local_audit.db"
SYNC_FILE_PATH = "hardware_sync_payload.txt"

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

def ingest_payload():
    init_db()
    
    if not os.path.exists(SYNC_FILE_PATH):
        print(f"[INFO] No hardware sync payload found at '{SYNC_FILE_PATH}'.")
        print("[INFO] Creating a mock/sample hardware sync payload for testing...")
        
        # Write a sample payload simulating Samsung Keystore TEE export
        with open(SYNC_FILE_PATH, "w") as f:
            f.write("0x06D217600c97129c47418F12289A8B7D44cFCaa0,m/44'/60'/0'/0/0")
            
    with open(SYNC_FILE_PATH, "r") as f:
        line = f.readline().strip()
        
    if not line or "," not in line:
        print("[ERROR] Invalid or empty sync payload format.")
        return
        
    address, hd_path = line.split(",", 1)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    timestamp = datetime.now(timezone.utc).isoformat()
    cursor.execute('''
        INSERT INTO parsed_records 
        (source_institution, ip_id, asset_title, asset_class, valuation, compliance_standard, status, ingested_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        "Samsung-Keystore-TEE",
        address[:12] + "...",
        f"HD-Path: {hd_path}",
        "Hardware-Wallet-ETH",
        0.0,
        "BIP-39/ScwService",
        "SYNCED",
        timestamp
    ))
    
    conn.commit()
    conn.close()
    print(f"[SUCCESS] Ingested hardware address {address} (Path: {hd_path}) into SQLite audit database.")

if __name__ == "__main__":
    ingest_payload()
