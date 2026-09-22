import sqlite3
from datetime import datetime, timezone

DB_PATH = "local_audit.db"

def log_hardware_address(address, hd_path, coin_type="ETH"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Ensure table exists
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
    
    timestamp = datetime.now(timezone.utc).isoformat()
    cursor.execute('''
        INSERT INTO parsed_records 
        (source_institution, ip_id, asset_title, asset_class, valuation, compliance_standard, status, ingested_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        "Samsung-Keystore-TEE",
        address[:12] + "...",
        f"HD-Path: {hd_path}",
        f"Hardware-Wallet-{coin_type}",
        0.0,
        "BIP-39/ScwService",
        "SECURED",
        timestamp
    ))
    
    conn.commit()
    conn.close()
    print(f"[SUCCESS] Logged hardware-backed address {address} ({hd_path}) into SQLite ledger.")

if __name__ == "__main__":
    # Example integration hook for a hardware-derived address
    sample_hw_address = "0x06D217600c97129c47418F12289A8B7D44cFCaa0"
    sample_hd_path = "m/44'/60'/0'/0/0"
    log_hardware_address(sample_hw_address, sample_hd_path)
