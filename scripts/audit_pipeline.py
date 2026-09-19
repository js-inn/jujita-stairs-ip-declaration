import json
import sqlite3
import hashlib
import hmac
import os
from datetime import datetime

DB_PATH = "local_audit.db"
MANIFEST_PATH = "manifests/dapp-manifest.json"

def init_db():
    """Initialize the local SQLite ledger database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            manifest_hash TEXT,
            status TEXT
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

    # Convert dictionary to a canonical JSON string for consistent hashing
    manifest_str = json.dumps(manifest_data, sort_keys=True)

    # Generate cryptographic checksum
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
    timestamp = datetime.utcnow().isoformat()

    cursor.execute('''
        INSERT INTO audit_logs (timestamp, manifest_hash, status)
        VALUES (?, ?, ?)
    ''', (timestamp, manifest_hash, "VERIFIED"))

    conn.commit()
    conn.close()
    print(f"[LEDGER] Audit record anchored to local SQLite database at {timestamp}")

if __name__ == "__main__":
    print("Initializing Local Audit Pipeline...")
    init_db()
    h = audit_manifest()
    log_to_ledger(h)

