import sqlite3
import json
import hmac
import hashlib
import time

class LocalCustodianNode:
    def __init__(self, db_path="local_custodian.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS local_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                metadata TEXT,
                vector_hash TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def ingest_and_embed(self, raw_data: str, secret_key: bytes):
        timestamp = time.time()
        # Simulate local embedding hash generation
        vector_hash = hmac.new(
            secret_key, 
            raw_data.encode('utf-8'), 
            hashlib.sha256
        ).hexdigest()
        
        metadata = json.dumps({"status": "localized", "length": len(raw_data)})

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO local_logs (timestamp, metadata, vector_hash) VALUES (?, ?, ?)",
            (timestamp, metadata, vector_hash)
        )
        conn.commit()
        conn.close()
        print(f"[Local Custodian] Data securely ingested. Vector Hash: {vector_hash[:12]}...")

if __name__ == "__main__":
    node = LocalCustodianNode()
    node.ingest_and_embed("Sample telemetry stream or local document text.", b"secure-edge-secret")

