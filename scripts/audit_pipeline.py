import json
import sqlite3
import hashlib
import os
import csv
from datetime import datetime, UTC

DB_PATH = "local_audit.db"
MANIFEST_PATH = "manifests/dapp-manifest.json"
DATA_DIR = "data"  # Directory for incoming multi-institution datasets

def init_db():
    """Initialize the local SQLite ledger database with audit and dataset tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Audit logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            manifest_hash TEXT,
            status TEXT
        )
    ''')
    
    # Financial/Prospectus parsed records table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parsed_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_institution TEXT,
            record_identifier TEXT,
            payload_data TEXT,
            ingested_at TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def audit_manifest():
    """Parse the local JSON manifest and generate an integrity hash."""
    if not os.path.exists(MANIFEST_PATH):
        print(f"Error: Manifest not found at {MANIFEST_PATH}")
        return None

    with open(MANIFEST_PATH, 'r') as f:
        manifest_data = json.load(f)

    manifest_str = json.dumps(manifest_data, sort_keys=True)
    manifest_hash = hashlib.sha256(manifest_str.encode('utf-8')).hexdigest()
    
    print(f"[SUCCESS] Manifest parsed successfully.")
    print(f"[PROVENANCE HASH] {manifest_hash}")
    return manifest_hash

def log_to_ledger(manifest_hash):
    """Anchor the audit record into the local SQLite ledger."""
    if not manifest_hash:
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now(UTC).isoformat()
    
    cursor.execute('''
        INSERT INTO audit_logs (timestamp, manifest_hash, status)
        VALUES (?, ?, ?)
    ''', (timestamp, manifest_hash, "VERIFIED"))
    
    conn.commit()
    conn.close()
    print(f"[LEDGER] Audit record anchored to local SQLite database at {timestamp}")

def parse_financial_datasets():
    """Scan the data directory for multi-institution CSV files and ingest them."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"[INFO] Created '{DATA_DIR}/' directory for incoming datasets.")
        print(f"[INFO] Place CSV prospectus files inside '{DATA_DIR}/' to parse them automatically.")
        return

    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    if not files:
        print(f"[INFO] No CSV datasets found in '{DATA_DIR}/' to parse.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    ingested_count = 0

    for file_name in files:
        file_path = os.path.join(DATA_DIR, file_name)
        institution_name = file_name.split('.')[0]
        
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                record_id = row.get('id', row.get('reference', 'UNKNOWN'))
                cursor.execute('''
                    INSERT INTO parsed_records (source_institution, record_identifier, payload_data, ingested_at)
                    VALUES (?, ?, ?, ?)
                ''', (institution_name, str(record_id), json.dumps(row), datetime.now(UTC).isoformat()))
                ingested_count += 1

    conn.commit()
    conn.close()
    print(f"[PARSER] Successfully ingested {ingested_count} records from multi-institution datasets.")

if __name__ == "__main__":
    print("Initializing Expanded Local Audit & Parsing Pipeline...")
    init_db()
    h = audit_manifest()
    log_to_ledger(h)
    parse_financial_datasets()


